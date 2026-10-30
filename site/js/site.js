/* Mesa Animal Rescue: mobile nav, the adoption filter and the contact form. */
(function () {
  "use strict";

  /* ---- Form delivery ------------------------------------------------------
     Set FORM_ENDPOINT to a form service URL (e.g. https://formspree.io/f/xxxx)
     to receive messages directly. Left empty, the form opens the visitor's
     mail app addressed to CONTACT_EMAIL instead. */
  var FORM_ENDPOINT = "";
  var CONTACT_EMAIL = "hello@mesarescue.example";

  var menuBtn = document.querySelector(".menu-btn");
  function setMenu(open) {
    document.body.classList.toggle("nav-open", open);
    menuBtn.setAttribute("aria-expanded", String(open));
  }
  menuBtn.addEventListener("click", function () { setMenu(!document.body.classList.contains("nav-open")); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && document.body.classList.contains("nav-open")) { setMenu(false); menuBtn.focus(); }
  });

  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---- Adoption filter ---- */
  var chips = document.querySelectorAll(".chip");
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var f = chip.dataset.filter, shown = 0;
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c === chip)); });
      document.querySelectorAll(".pet[data-species]").forEach(function (p) {
        var on = f === "all" || p.dataset.species === f;
        p.hidden = !on;
        if (on) shown++;
      });
      document.querySelector(".empty").hidden = shown > 0;
    });
  });

  /* ---- Contact form ---- */
  var form = document.querySelector("#ask-form");
  if (!form) return;
  var status = form.querySelector(".status");
  var about = new URLSearchParams(window.location.search).get("about");
  if (about) {
    Array.prototype.forEach.call(form.elements.about.options, function (o) { if (o.text === about) form.elements.about.value = o.value; });
  }

  function show(kind, text) {
    status.className = "status field-wide " + kind;
    status.textContent = text;
    status.hidden = false;
  }

  function mailto(data) {
    var body = Object.keys(data).map(function (k) { return k + ": " + data[k]; }).join("\n");
    window.location.href = "mailto:" + CONTACT_EMAIL + "?subject=" + encodeURIComponent("Question about " + data.about) + "&body=" + encodeURIComponent(body);
    show("ok", "Your mail app should open with your message filled in. If it doesn't, email " + CONTACT_EMAIL + " or call (480) 555-0179.");
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var invalid = Array.prototype.filter.call(form.elements, function (el) {
      var bad = el.willValidate && !el.checkValidity();
      if (el.willValidate) el.setAttribute("aria-invalid", String(bad));
      return bad;
    });
    if (invalid.length) {
      show("err", "Please fill in: " + invalid.map(function (el) { return el.dataset.name; }).join(", ") + ".");
      invalid[0].focus();
      return;
    }
    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });
    if (!FORM_ENDPOINT) { mailto(data); return; }
    var btn = form.querySelector("button[type=submit]");
    btn.disabled = true;
    fetch(FORM_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data) })
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        form.reset();
        show("ok", "Thank you. We'll reply within two days.");
      })
      .catch(function () {
        show("err", "That didn't send. Opening your mail app instead.");
        mailto(data);
      })
      .then(function () { btn.disabled = false; });
  });
})();
