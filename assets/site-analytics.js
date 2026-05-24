(function () {
  "use strict";

  if (window.__MYMIRROR_SITE_ANALYTICS__) return;
  window.__MYMIRROR_SITE_ANALYTICS__ = true;

  var MEASUREMENT_ID = "G-QR2SPD4MZM";
  var CLICK_NAV_DELAY_MS = 320;
  var scrollMarks = [25, 50, 75, 90];
  var sentScrollMarks = {};
  var engagementStartedAt = Date.now();

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };

  if (!document.querySelector('script[src*="googletagmanager.com/gtag/js?id=' + MEASUREMENT_ID + '"]')) {
    var gaScript = document.createElement("script");
    gaScript.async = true;
    gaScript.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(MEASUREMENT_ID);
    document.head.appendChild(gaScript);
  }

  window.gtag("js", new Date());
  window.gtag("config", MEASUREMENT_ID, {
    transport_type: "beacon"
  });

  function cleanText(value, fallback, maxLength) {
    var text = String(value || fallback || "unknown")
      .trim()
      .toLowerCase()
      .replace(/[^a-z0-9_ -]+/g, "")
      .replace(/\s+/g, "_")
      .slice(0, maxLength || 95);
    return text || fallback || "unknown";
  }

  function visibleText(element, maxLength) {
    return String((element && element.innerText) || "")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, maxLength || 90);
  }

  function pageSlug() {
    var path = window.location.pathname || "/";
    path = path.replace(/\/index\.html$/i, "/").replace(/\/$/, "");
    if (!path || path === "") return "home";
    return cleanText(path.replace(/^\/+/, "").replace(/\//g, "_"), "home", 80);
  }

  function canonicalPath() {
    var canonical = document.querySelector('link[rel="canonical"]');
    if (!canonical || !canonical.href) return window.location.pathname || "/";
    try {
      return new URL(canonical.href, window.location.href).pathname || "/";
    } catch (_) {
      return window.location.pathname || "/";
    }
  }

  function contentGroup() {
    var path = window.location.pathname || "/";
    if (path === "/" || /index\.html$/i.test(path)) return path.indexOf("/acne/") === 0 ? "seo_acne_hub" : "seo_home";
    if (path.indexOf("/acne/") === 0) return "seo_acne";
    if (path.indexOf("face-map-experiment") !== -1) return "seo_face_map_experiment";
    return "seo_static";
  }

  function deviceCategory() {
    var width = window.innerWidth || 0;
    if (width < 768) return "mobile";
    if (width < 1024) return "tablet";
    return "desktop";
  }

  function commonParams() {
    return {
      app_area: "seo_pages",
      page_slug: pageSlug(),
      content_group: contentGroup(),
      canonical_path: canonicalPath().slice(0, 100),
      device_category: deviceCategory(),
      engagement_time_msec: Math.max(1, Math.min(Date.now() - engagementStartedAt, 600000))
    };
  }

  function referrerDomain() {
    if (!document.referrer) return "direct";
    try {
      return cleanText(new URL(document.referrer).hostname, "direct", 80);
    } catch (_) {
      return "unknown";
    }
  }

  function safeParams(params) {
    var merged = Object.assign(commonParams(), params || {});
    var cleaned = {};
    Object.keys(merged).slice(0, 25).forEach(function (key) {
      var value = merged[key];
      if (value === null || value === undefined || value === "") return;
      var safeKey = String(key).replace(/[^a-zA-Z0-9_]/g, "_").slice(0, 40);
      if (!safeKey) return;
      if (typeof value === "number") {
        if (Number.isFinite(value)) cleaned[safeKey] = Math.round(value);
      } else if (typeof value === "boolean") {
        cleaned[safeKey] = value ? "yes" : "no";
      } else {
        cleaned[safeKey] = String(value).slice(0, 100);
      }
    });
    return cleaned;
  }

  function track(eventName, params, options) {
    if (typeof window.gtag !== "function") return;
    var payload = safeParams(params);
    if (options && typeof options.callback === "function") {
      payload.event_callback = options.callback;
      payload.event_timeout = options.timeout || CLICK_NAV_DELAY_MS;
    }
    window.gtag("event", String(eventName).slice(0, 40), payload);
  }

  function linkUrl(anchor) {
    try {
      return new URL(anchor.getAttribute("href"), window.location.href);
    } catch (_) {
      return null;
    }
  }

  function linkLocation(anchor) {
    if (anchor.closest("nav")) return "nav";
    if (anchor.closest("header")) return "hero";
    if (anchor.closest("footer")) return "footer";
    if (anchor.closest("aside") || anchor.closest(".sidebar")) return "sidebar";
    var section = anchor.closest("section[id], article[id], div[id]");
    if (section && section.id) return cleanText(section.id, "section", 50);
    return "body";
  }

  function destinationType(url) {
    if (!url) return "unknown";
    var samePageHash = url.origin === window.location.origin &&
      url.pathname === window.location.pathname &&
      !!url.hash;
    if (samePageHash) return "anchor";
    if (url.pathname === "/scan" || url.pathname === "/scan/" || url.hostname.indexOf("face3layerscanner") !== -1) return "scanner";
    if (url.pathname.indexOf("/acne/face-map") === 0 || url.pathname.indexOf("face-map-experiment") !== -1) return "face_map";
    if (url.origin === window.location.origin || url.hostname === "mymirror.fit") return "internal";
    return "outbound";
  }

  function isCta(anchor, type) {
    var classes = cleanText(anchor.className || "", "", 120);
    var text = cleanText(visibleText(anchor, 90), "", 90);
    return type === "scanner" ||
      /cta|btn|button|face_ai|nav_cta|sidebar_cta|premium/.test(classes) ||
      /skin_analysis|free_analysis|start_free|try_free|scan|check_your_skin|start_analysis/.test(text);
  }

  function isGuideLink(anchor) {
    var classes = cleanText(anchor.className || "", "", 120);
    return /guide_link|related|sidebar|toc_link|nav/.test(classes) || !!anchor.closest("nav");
  }

  function linkParams(anchor, url, type) {
    return {
      link_type: type,
      link_url: url ? (url.pathname + url.search + url.hash).slice(0, 100) : "unknown",
      link_domain: url ? url.hostname.slice(0, 80) : "unknown",
      link_text: visibleText(anchor, 80),
      cta_location: linkLocation(anchor),
      cta_class: cleanText(anchor.className || "none", "none", 80)
    };
  }

  function scanUrlWithAttribution(url, anchor) {
    var next = new URL(url.href);
    var slug = pageSlug();
    if (!next.searchParams.has("utm_source")) next.searchParams.set("utm_source", "seo");
    if (!next.searchParams.has("utm_medium")) next.searchParams.set("utm_medium", "site_cta");
    if (!next.searchParams.has("utm_campaign")) next.searchParams.set("utm_campaign", "skin_scan");
    if (!next.searchParams.has("utm_content")) next.searchParams.set("utm_content", slug);
    if (!next.searchParams.has("source")) next.searchParams.set("source", "seo_" + slug);
    next.searchParams.set("entry_page", slug);
    next.searchParams.set("cta_location", linkLocation(anchor));
    return next.href;
  }

  function shouldOwnNavigation(event, anchor, type) {
    return type === "scanner" &&
      event.button === 0 &&
      !event.metaKey &&
      !event.ctrlKey &&
      !event.shiftKey &&
      !event.altKey &&
      (!anchor.target || anchor.target === "_self");
  }

  function handleClick(event) {
    var anchor = event.target && event.target.closest ? event.target.closest("a[href]") : null;
    if (!anchor) return;
    var url = linkUrl(anchor);
    var type = destinationType(url);
    var cta = isCta(anchor, type);
    var guide = isGuideLink(anchor);
    var params = linkParams(anchor, url, type);

    if (cta) {
      track("seo_cta_click", Object.assign({ cta_type: type }, params));
    } else if (type === "anchor" || anchor.classList.contains("toc-link")) {
      track("seo_toc_click", params);
    } else if (guide || type === "outbound") {
      track("seo_link_click", params);
    } else {
      return;
    }

    if (type === "face_map") {
      track("seo_face_map_click", params);
    }

    if (type !== "scanner" || !url) return;

    var nextHref = scanUrlWithAttribution(url, anchor);
    anchor.href = nextHref;
    var navigate = function () {
      window.location.href = nextHref;
    };

    if (shouldOwnNavigation(event, anchor, type)) {
      event.preventDefault();
      var navigated = false;
      var safeNavigate = function () {
        if (navigated) return;
        navigated = true;
        navigate();
      };
      track("seo_scan_cta_click", params, { callback: safeNavigate, timeout: CLICK_NAV_DELAY_MS });
      window.setTimeout(safeNavigate, CLICK_NAV_DELAY_MS + 80);
    } else {
      track("seo_scan_cta_click", params);
    }
  }

  function currentScrollPercent() {
    var doc = document.documentElement;
    var body = document.body;
    var scrollTop = window.pageYOffset || doc.scrollTop || body.scrollTop || 0;
    var height = Math.max(
      body.scrollHeight || 0,
      doc.scrollHeight || 0,
      body.offsetHeight || 0,
      doc.offsetHeight || 0
    ) - window.innerHeight;
    if (height <= 0) return 100;
    return Math.min(100, Math.round((scrollTop / height) * 100));
  }

  function handleScroll() {
    var percent = currentScrollPercent();
    scrollMarks.forEach(function (mark) {
      if (!sentScrollMarks[mark] && percent >= mark) {
        sentScrollMarks[mark] = true;
        track("seo_scroll_depth", { scroll_percent: mark });
      }
    });
  }

  function init() {
    track("seo_page_view", {
      page_title: document.title.slice(0, 100),
      referrer_domain: referrerDomain()
    });
    document.addEventListener("click", handleClick, true);
    window.addEventListener("scroll", handleScroll, { passive: true });
    window.setTimeout(function () {
      track("seo_page_engaged", { engaged_seconds: 15 });
    }, 15000);
    handleScroll();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
