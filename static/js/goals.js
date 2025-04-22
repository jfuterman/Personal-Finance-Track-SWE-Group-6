document.addEventListener('DOMContentLoaded', () => {
  const modalEl       = document.getElementById('goalModal');
  const bsModal       = new bootstrap.Modal(modalEl);
  const form          = document.getElementById('goalForm');
  const modalLabel    = document.getElementById('goalModalLabel');
  const modalAction   = document.getElementById('modalAction');
  const inputTitle    = document.getElementById('modalTitle');
  const inputMonthly  = document.getElementById('modalMonthly');
  const inputAchieved = document.getElementById('modalAchieved');
  const fieldTitle    = document.getElementById('field-title');
  const errorEl       = document.getElementById('modalError');

  document.querySelectorAll('.progress-bar[data-progress]').forEach(bar => {
    const pct = bar.dataset.progress;
    bar.style.width = `${pct}%`;
    bar.setAttribute('aria-valuenow', pct);
  });

  form.addEventListener('submit', (e) => {
    errorEl.style.display = 'none';
    const monthly = parseFloat(inputMonthly.value)  || 0;
    const achieved= parseFloat(inputAchieved.value) || 0;

    if (achieved > monthly) {
      e.preventDefault();
      errorEl.textContent = '❌ Achieved amount cannot exceed monthly target.';
      errorEl.style.display = 'block';
    }
  });

  // + Add Goal
  document.getElementById('add-goal-btn').addEventListener('click', (e) => {
    form.action           = e.currentTarget.dataset.url;
    modalLabel.textContent= 'Add Goal';
    modalAction.value     = 'add';

    fieldTitle.style.display = 'block';
    inputTitle.required      = true;

    inputTitle.value     = '';
    inputMonthly.value   = '';
    inputAchieved.value  = '';
    errorEl.style.display = 'none';

    bsModal.show();
  });

  document.querySelectorAll('.edit-goal-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      form.action           = btn.dataset.url;
      modalLabel.textContent= 'Edit Goal';
      modalAction.value     = 'edit';

      fieldTitle.style.display = 'block';
      inputTitle.required      = true;

      inputTitle.value     = btn.dataset.title;
      inputMonthly.value   = btn.dataset.monthly;
      inputAchieved.value  = btn.dataset.achieved;
      errorEl.style.display = 'none';

      bsModal.show();
    });
  });

  const delModalEl = document.getElementById('deleteConfirmModal');
  const delModal   = new bootstrap.Modal(delModalEl);
  const delForm    = document.getElementById('deleteConfirmForm');
  document.querySelectorAll('.delete-goal-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      delForm.action = btn.dataset.url;
      delModal.show();
    });
  });
});
