const fileInput = document.getElementById('file-input');
const folderInput = document.getElementById('folder-input');
const note = document.getElementById('notification');

[fileInput, folderInput].forEach(input => {
    input.addEventListener('change', async () => {
        const files = input.files;
        if (!files.length) return;

        note.textContent = "Uploading...";
        note.className = "text-blue-700";
        note.classList.remove("hidden");

        const formData = new FormData();
        for (const file of files) {
            formData.append('files', file, file.webkitRelativePath || file.name);
        }

        try {
            const res = await fetch('/upload', { method: 'POST', body: formData });
            const json = await res.json();

            if (json.success) {
                note.textContent = "✅ Uploaded successfully!";
                note.className = "text-green-700";
            } else {
                throw new Error(json.message || "Upload failed");
            }
        } catch (e) {
            note.textContent = "❌ " + e.message;
            note.className = "text-red-700";
        }

        input.value = ""; // reset input
    });
});
