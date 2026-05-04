const toggleBodyComposition = document.getElementById('toggleBodyComposition');
const bodyCompositionFields = document.getElementById('bodyCompositionFields');
if (toggleBodyComposition && bodyCompositionFields) {
    toggleBodyComposition.addEventListener('change', () => {
        bodyCompositionFields.classList.toggle('d-none', !toggleBodyComposition.checked);
    });
}

const trainingModal = document.getElementById('trainingModal');
const modalButtons = document.querySelectorAll('#open-training-modal, #close-training-modal, #close-training-footer');
const bodyClass = document.body.classList;

const toggleModal = show => {
    if (!trainingModal) return;
    trainingModal.classList.toggle('d-none', !show);
    trainingModal.classList.toggle('show', show);
    bodyClass.toggle('modal-open', show);
    document.body.style.overflow = show ? 'hidden' : '';
};

modalButtons.forEach(button => {
    if (!button) return;
    button.addEventListener('click', event => {
        if (button.id === 'open-training-modal') {
            event.preventDefault();
            toggleModal(true);
        } else {
            toggleModal(false);
        }
    });
});

const tabs = document.querySelectorAll('#trainingTab button');
const panes = document.querySelectorAll('.training-tab-pane');
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(btn => btn.classList.remove('active'));
        panes.forEach(pane => pane.classList.add('d-none'));
        tab.classList.add('active');
        const target = document.getElementById(tab.dataset.tabTarget);
        if (target) target.classList.remove('d-none');
    });
});

const rmRepsInput = document.getElementById('rmReps');
const rmCalculatorResult = document.getElementById('rmCalculatorResult');
const baseWeight = window.baseWeight || 0;

if (rmRepsInput && rmCalculatorResult) {
    const updateRMDisplay = () => {
        const reps = parseInt(rmRepsInput.value, 10) || 5;
        const estimatedLoad = ((baseWeight * 1.3) / (1 + reps / 30)).toFixed(1);
        rmCalculatorResult.innerHTML = `Estimación de carga para ${reps} repeticiones: <strong>${estimatedLoad} kg</strong>`;
    };
    rmRepsInput.addEventListener('input', updateRMDisplay);
    updateRMDisplay();
}

if (trainingModal) {
    trainingModal.addEventListener('click', event => {
        if (event.target === trainingModal) {
            toggleModal(false);
        }
    });
}
