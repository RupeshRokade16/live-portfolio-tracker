console.clear();
(function () {
  'use strict';

  const preventDefaults = (event) => {
    event.preventDefault();
    event.stopPropagation();
  };

  const highlight = (event) =>
    event.target.classList.add('highlight');

  const unhighlight = (event) =>
    event.target.classList.remove('highlight');

  const isCSVFile = (file) =>
    file.type === 'text/csv' || file.name.endsWith('.csv');

  const previewCSVFile = (file, gallery) => {
    const csvIcon = document.createElement('div');
    csvIcon.className = 'upload_img mt-2';
    csvIcon.textContent = `📄 ${file.name}`;
    gallery.appendChild(csvIcon);
  };

  const handleDrop = (event) => {
    const zone = event.target.closest('.upload_dropZone');
    const input = zone.querySelector('input[type="file"]');
    const gallery = zone.querySelector('.upload_gallery');
    const files = [...event.dataTransfer.files];

    const csvFiles = files.filter(isCSVFile);
    if (!csvFiles.length) return alert('Only CSV files are allowed!');

    previewCSVFile(csvFiles[0], gallery);
    input.files = new DataTransfer().items.add(csvFiles[0]);
  };

  const setupDropZones = () => {
    const dropZones = document.querySelectorAll('.upload_dropZone');

    dropZones.forEach((zone) => {
      ;['dragenter', 'dragover'].forEach((event) =>
        zone.addEventListener(event, highlight, false)
      );
      ;['dragleave', 'drop'].forEach((event) =>
        zone.addEventListener(event, unhighlight, false)
      );
      zone.addEventListener('drop', handleDrop, false);

      const input = zone.querySelector('input[type="file"]');
      const gallery = zone.querySelector('.upload_gallery');

      input.addEventListener('change', (event) => {
        const files = [...event.target.files];
        if (!files.length || !isCSVFile(files[0]))
          return alert('Only CSV files are allowed!');

        gallery.innerHTML = '';
        previewCSVFile(files[0], gallery);
      });
    });
  };

  document.addEventListener('DOMContentLoaded', setupDropZones);
})();
