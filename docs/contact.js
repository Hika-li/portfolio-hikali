(function () {
  var form = document.getElementById("contact-form");
  var status = form.querySelector(".form-status");
  var button = form.querySelector('button[type="submit"]');

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (form._honey.value) return;
    var data = Object.fromEntries(new FormData(form));
    data._subject = "Portfolio: " + data.topic + " (" + data.name + ")";
    data._replyto = data.email;
    button.disabled = true;
    status.className = "form-status";
    status.textContent = form.dataset.sending;
    fetch("https://formsubmit.co/ajax/sabri.mohamadi@outlook.fr", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(data)
    })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok || j.success === "false" || j.success === false) throw j; }); })
      .then(function () {
        form.reset();
        status.className = "form-status ok";
        status.textContent = form.dataset.ok;
      })
      .catch(function (j) {
        status.className = "form-status err";
        var pending = j && /activ/i.test(j.message || "");
        status.textContent = pending ? form.dataset.activate : form.dataset.err;
      })
      .finally(function () { button.disabled = false; });
  });
})();
