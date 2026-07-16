/* Basilica Audio — latest-release download buttons.
 *
 * Fetches the latest GitHub release for this plugin and replaces the static
 * fallback link with one download button per .zip asset (version / size / date).
 * On any failure (offline, rate-limited, no release yet) the server-rendered
 * fallback link to the GitHub releases page simply stays in place.
 *
 * The GitHub org login is injected once by build.py into <body data-org="...">
 * — single source of truth, survives the upcoming org rename. The one piece
 * of chrome copy this script renders ("Release notes & previous versions")
 * is likewise injected per-page via data-release-notes-label on the
 * data-repo section, sourced from build.py's STRINGS dict, so the German
 * pages get the localized label too.
 */
(function () {
  "use strict";

  var ORG = document.body.dataset.org;
  var section = document.querySelector("section[data-repo]");
  if (!ORG || !section) { return; }

  var repo = section.dataset.repo;
  var area = document.getElementById("download-area");
  if (!repo || !area) { return; }

  var releasesPage = "https://github.com/" + ORG + "/" + repo + "/releases";

  function humanSize(bytes) {
    if (typeof bytes !== "number" || bytes <= 0) { return ""; }
    if (bytes < 1024 * 1024) { return (bytes / 1024).toFixed(0) + " KB"; }
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  }

  function humanDate(iso) {
    var d = new Date(iso);
    if (isNaN(d.getTime())) { return ""; }
    return d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
  }

  function platformOf(assetName) {
    var n = assetName.toLowerCase();
    if (n.indexOf("macos") !== -1 || n.indexOf("darwin") !== -1 || n.indexOf("-mac") !== -1) {
      return { label: "macOS", rank: 0 };
    }
    if (n.indexOf("windows") !== -1 || n.indexOf("win64") !== -1 || n.indexOf("win32") !== -1) {
      return { label: "Windows", rank: 1 };
    }
    if (n.indexOf("linux") !== -1) { return { label: "Linux", rank: 2 }; }
    return { label: assetName, rank: 3 };
  }

  function render(release, zips) {
    var version = release.tag_name || release.name || "";
    var date = humanDate(release.published_at);

    var wrap = document.createElement("div");
    wrap.className = "download-buttons";

    zips
      .map(function (asset) {
        var p = platformOf(asset.name);
        return { asset: asset, label: p.label, rank: p.rank };
      })
      .sort(function (a, b) { return a.rank - b.rank; })
      .forEach(function (entry) {
        var a = document.createElement("a");
        a.className = "dl-btn";
        a.href = entry.asset.browser_download_url;

        var platform = document.createElement("span");
        platform.className = "dl-platform";
        platform.textContent = entry.label;

        var meta = document.createElement("span");
        meta.className = "dl-meta";
        meta.textContent = [version, humanSize(entry.asset.size), date]
          .filter(Boolean).join(" · ");

        var file = document.createElement("span");
        file.className = "dl-file";
        file.textContent = entry.asset.name;

        a.appendChild(platform);
        a.appendChild(meta);
        a.appendChild(file);
        wrap.appendChild(a);
      });

    var more = document.createElement("p");
    more.className = "dl-release-link";
    var moreLink = document.createElement("a");
    moreLink.href = releasesPage;
    moreLink.rel = "noopener";
    moreLink.textContent = section.dataset.releaseNotesLabel || "Release notes & previous versions";
    more.appendChild(moreLink);

    area.textContent = "";
    area.appendChild(wrap);
    area.appendChild(more);
  }

  fetch("https://api.github.com/repos/" + ORG + "/" + repo + "/releases/latest", {
    headers: { Accept: "application/vnd.github+json" }
  })
    .then(function (response) {
      if (!response.ok) { throw new Error("HTTP " + response.status); }
      return response.json();
    })
    .then(function (release) {
      var zips = (release.assets || []).filter(function (asset) {
        return /\.zip$/i.test(asset.name);
      });
      if (zips.length === 0) { return; } // keep the fallback link
      render(release, zips);
    })
    .catch(function () { /* keep the fallback link */ });
})();
