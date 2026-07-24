using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using BepInEx;
using HarmonyLib;
using TMPro;
using UnityEngine;
using UnityEngine.TextCore.LowLevel;

namespace DatabaseDetective.PTBR
{
    // Registers a pixel font that HAS Portuguese accents as a global TextMeshPro
    // fallback, so accented characters (á ã ç é õ ú ...) render in a matching
    // pixel style instead of the game's ASCII-only atlas falling back to a smooth font.
    //
    // Also forces word-wrapping on long translated text so Portuguese (which is
    // longer than English, and whose machine-translated lines may lack the original
    // hard line breaks) wraps inside its window instead of overflowing the HUD.
    [BepInPlugin("com.ptbr.databasedetective.font", "Database Detective PT-BR Accent Font", "1.0.0")]
    public class PtbrFontPlugin : BaseUnityPlugin
    {
        private void Awake()
        {
            StartCoroutine(SetupWhenReady());
            try
            {
                new Harmony("com.ptbr.databasedetective.font").PatchAll(typeof(WrapPatch));
                Logger.LogInfo("[PT-BR] Word-wrap patch applied.");
            }
            catch (Exception e) { Logger.LogWarning("[PT-BR] Word-wrap patch failed: " + e.Message); }
        }

        private IEnumerator SetupWhenReady()
        {
            // Wait until TextMeshPro settings are available.
            float timeout = 30f;
            while (TMP_Settings.instance == null && timeout > 0f)
            {
                timeout -= Time.unscaledDeltaTime;
                yield return null;
            }
            // A couple extra frames so TMP is fully initialized.
            yield return null;
            yield return null;

            TMP_FontAsset fallback = null;
            try
            {
                string dir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
                string ttf = Path.Combine(dir, "PixelifySans.ttf");
                if (!File.Exists(ttf))
                {
                    Logger.LogError("[PT-BR] Accent font TTF not found: " + ttf);
                    yield break;
                }

                // Create a DYNAMIC font asset straight from the .ttf on disk (no OS install needed).
                fallback = TMP_FontAsset.CreateFontAsset(ttf, 0, 90, 9, GlyphRenderMode.SDFAA, 1024, 1024);
                if (fallback == null)
                {
                    Logger.LogError("[PT-BR] CreateFontAsset returned null.");
                    yield break;
                }
                fallback.name = "PTBR Accent Fallback (Pixelify Sans)";
                fallback.atlasPopulationMode = AtlasPopulationMode.Dynamic;
                UnityEngine.Object.DontDestroyOnLoad(fallback);

                RegisterGlobalFallback(fallback);
                Logger.LogInfo("[PT-BR] Pixel accent fallback font registered globally.");
            }
            finally { }
        }

        private void RegisterGlobalFallback(TMP_FontAsset fallback)
        {
            // 1) Global TMP fallback list (final fallback for every TMP text component).
            List<TMP_FontAsset> list = TMP_Settings.fallbackFontAssets;
            if (list == null)
            {
                list = new List<TMP_FontAsset>();
                var f = typeof(TMP_Settings).GetField("m_fallbackFontAssets",
                    BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public);
                if (f != null && TMP_Settings.instance != null)
                    f.SetValue(TMP_Settings.instance, list);
            }
            if (!list.Contains(fallback))
                list.Add(fallback);

            // 2) Also attach to the default font asset's own fallback table, belt-and-suspenders.
            var def = TMP_Settings.defaultFontAsset;
            if (def != null)
            {
                if (def.fallbackFontAssetTable == null)
                    def.fallbackFontAssetTable = new List<TMP_FontAsset>();
                if (!def.fallbackFontAssetTable.Contains(fallback))
                    def.fallbackFontAssetTable.Add(fallback);
            }
        }
    }

    // Forces word-wrapping on long text blocks so translated (longer) Portuguese text
    // wraps within its window instead of running off the edge. Skips text input fields
    // (e.g. the SQL query box) so typing/scrolling behaviour is untouched.
    [HarmonyPatch(typeof(TMP_Text), "set_text", new Type[] { typeof(string) })]
    internal static class WrapPatch
    {
        private static readonly HashSet<int> skip = new HashSet<int>();
        private static readonly HashSet<int> handled = new HashSet<int>();

        private static void Postfix(TMP_Text __instance, string value)
        {
            if (__instance == null || value == null) return;
            if (value.Length < 16) return;            // leave very short labels alone
            if (value.IndexOf(' ') < 0) return;       // single tokens (data) untouched
            int id = __instance.GetInstanceID();
            if (skip.Contains(id) || handled.Contains(id)) return;
            try
            {
                // never touch input fields (the SQL query box, name entry, etc.)
                if (__instance.GetComponentInParent<TMP_InputField>() != null) { skip.Add(id); return; }
                if (!__instance.enableWordWrapping) __instance.enableWordWrapping = true;
                // Auto-shrink longer Portuguese text so it fits fixed-size boxes (speech
                // bubbles, popups) instead of spilling out. Only shrinks when it doesn't
                // fit; text that already fits stays at its original size. SDF fonts scale
                // cleanly so the pixel look is preserved.
                if (!__instance.enableAutoSizing)
                {
                    float baseSize = __instance.fontSize;
                    if (baseSize > 1f)
                    {
                        __instance.fontSizeMax = baseSize;
                        __instance.fontSizeMin = Mathf.Max(6f, baseSize * 0.5f);
                        __instance.enableAutoSizing = true;
                    }
                }
                handled.Add(id);
            }
            catch { skip.Add(id); }
        }
    }
}
