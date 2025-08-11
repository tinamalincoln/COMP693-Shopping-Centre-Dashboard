

  // ---- Edit form change detection ----
  var form = document.getElementById('edit-form');
  var saveBtn = document.getElementById('save-btn');
  if (form && saveBtn) {
    var initialData = new FormData(form);
    var imageInput = form.querySelector('input[type="file"]');

    function isFormChanged() {
      var currentData = new FormData(form);

      // Compare simple fields
      for (var pair of currentData.entries()) {
        // Skip file input in this loop
        if (pair[0] === 'image') continue;
        if (initialData.get(pair[0]) !== pair[1]) return true;
      }
      // If an image is selected, that's a change
      if (imageInput && imageInput.files && imageInput.files.length > 0) return true;

      return false;
    }

    function refreshButtonState() {
      saveBtn.disabled = !isFormChanged();
    }

    form.addEventListener('input', refreshButtonState);
    if (imageInput) imageInput.addEventListener('change', refreshButtonState);
  }

