// File: frontend/static/js/version_check.js
// Purpose: Soft “hard refresh” — reload once when /static/version.txt changes.
// How it works:
// 1) Fetch /static/version.txt with no-store
// 2) If the version differs from last seen, redirect this page to add ?appv=<version>
//    so the HTML revalidates and assets are re-fetched without users needing a hard refresh.

(function () {
  const VERSION_URL = "/static/version.txt";
  const LS_KEY      = "ur_asset_version";
  const PARAM_NAME  = "appv";

  function setOnceInSession(key, val) {
    try { sessionStorage.setItem(key, val); } catch (_) {}
  }
  function getFromSession(key) {
    try { return sessionStorage.getItem(key); } catch (_) { return null; }
  }
  function setInLocal(key, val) {
    try { localStorage.setItem(key, val); } catch (_) {}
  }
  function getFromLocal(key) {
    try { return localStorage.getItem(key); } catch (_) { return null; }
  }

  function same(strA, strB) {
    return String(strA || "").trim() === String(strB || "").trim();
  }

  function currentParamVersion() {
    try {
      const u = new URL(window.location.href);
      return u.searchParams.get(PARAM_NAME);
    } catch (_) { return null; }
  }

  async function check() {
    try {
      const res = await fetch(VERSION_URL, { cache: "no-store" });
      if (!res.ok) return; // be quiet on failures
      const latest = (await res.text()).trim();
      if (!latest) return;

      const lastSeen = getFromLocal(LS_KEY);
      const urlVer   = currentParamVersion();

      // If URL already has this version AND local remembers it, do nothing.
      if (same(urlVer, latest) && same(lastSeen, latest)) return;

      // If this is the first run (no lastSeen), remember and do nothing.
      if (!lastSeen) {
        setInLocal(LS_KEY, latest);
        return;
      }

      // Version changed → update local and bounce once by appending ?appv=<version>
      const bouncedKey = "__ur_bounced_for_ver__";
      const alreadyBounced = same(getFromSession(bouncedKey), latest);
      setInLocal(LS_KEY, latest);

      if (!alreadyBounced) {
        setOnceInSession(bouncedKey, latest);
        const u = new URL(window.location.href);
        u.searchParams.set(PARAM_NAME, latest);
        window.location.replace(u.toString());
      }
    } catch (_) {
      // swallow; never break the page
    }
  }

  // Run ASAP
  check();
})();
