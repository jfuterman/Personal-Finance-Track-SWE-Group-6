document.addEventListener("DOMContentLoaded", () => {
  const modalEl = document.getElementById("goalModal");
  const bsModal = new bootstrap.Modal(modalEl);
  const form = document.getElementById("goalForm");
  const modalLabel = document.getElementById("goalModalLabel");
  const modalAction = document.getElementById("modalAction");
  const inputTitle = document.getElementById("modalTitle");
  const inputMonthly = document.getElementById("modalMonthly");
  const inputAchieved = document.getElementById("modalAchieved");
  const fieldTitle = document.getElementById("field-title");
  const errorEl = document.getElementById("modalError");
  const quickAddBtn = document.getElementById("quick-add-btn");

  document.querySelectorAll(".progress-bar[data-progress]").forEach((bar) => {
    const pct = bar.dataset.progress;
    bar.style.width = `${pct}%`;
    bar.setAttribute("aria-valuenow", pct);
  });

  form.addEventListener("submit", (e) => {
    const monthly = +inputMonthly.value.trim();
    const achieved = +inputAchieved.value.trim();
    let errorMsg = "";

    if (
      !monthly ||
      monthly <= 0 ||
      !Number.isFinite(monthly) ||
      !achieved ||
      achieved <= 0 ||
      !Number.isFinite(achieved)
    ) {
      errorMsg =
        "❌ Monthly amount or Achieved amount must be a number greater than 0.";
    }

    if (errorMsg) {
      e.preventDefault();
      errorEl.textContent = errorMsg;
      errorEl.style.display = "block";
    }
  });

  document.getElementById("add-goal-btn").addEventListener("click", (e) => {
    form.action = e.currentTarget.dataset.url;
    modalLabel.textContent = "Add Goal";
    modalAction.value = "add";

    fieldTitle.style.display = "block";
    inputTitle.required = true;

    inputTitle.value = "";
    inputMonthly.value = "";
    inputAchieved.value = "";
    errorEl.style.display = "none";

    quickAddBtn.style.display = "none";

    bsModal.show();
  });

  document.querySelectorAll(".edit-goal-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      form.action = btn.dataset.url;
      modalLabel.textContent = "Edit Goal";
      modalAction.value = "edit";

      fieldTitle.style.display = "block";
      inputTitle.required = true;

      inputTitle.value = btn.dataset.title;
      inputMonthly.value = parseFloat(btn.dataset.monthly);
      inputAchieved.value = parseFloat(btn.dataset.achieved);
      errorEl.style.display = "none";

      quickAddBtn.style.display = "inline-block";

      bsModal.show();
    });
  });

  document.querySelectorAll(".quick-add-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const increment = parseFloat(btn.dataset.add);
      inputAchieved.value = (parseFloat(inputAchieved.value) || 0) + increment;
    });
  });

  const delModalEl = document.getElementById("deleteConfirmModal");
  const delModal = new bootstrap.Modal(delModalEl);
  const delForm = document.getElementById("deleteConfirmForm");

  document.querySelectorAll(".delete-goal-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      delForm.action = btn.dataset.url;
      delModal.show();
    });
  });
});
