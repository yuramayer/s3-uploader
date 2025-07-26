// аналог BeatifulSoup.select('#id') - 
//      выбираем элементы на странице
const dropzone = document.getElementById('dropzone');
const input = document.getElementById('hidden-input');
const note = document.getElementById('notification');

// Хелпер — та же логика с загрузкой и спиннером
// асинхронная обёртка:
// показывает спиннер, ждёт promise,
// минимум 2.5 секунды ждёт
// и показывает v или x с текстом
async function showSpinnerDuring(promise) {
    note.innerHTML = '<div class="spinner"></div>';
    note.classList.remove('hidden');

    const MIN_TIME = 2500;
    const startTime = Date.now();

    const result = await promise.catch(err => ({ error: err }));

    const elapsed = Date.now() - startTime;
    if (elapsed < MIN_TIME) {
        await new Promise(res => setTimeout(res, MIN_TIME - elapsed));
    }

    if (result.error) {
        note.innerHTML = `❌ ${result.error.message}`;
        note.className = 'text-red-700 text-sm text-center mt-4 font-medium';
    } else {
        note.innerHTML = '✅ Uploaded successfully!';
        note.className = 'text-green-700 text-sm text-center mt-4 font-medium';
    }

    return result;
}

// fileList - аналог list[File] в js
function uploadFileList(fileList) {
    const formData = new FormData();
    for (const file of fileList) {
        formData.append('files', file, file.webkitRelativePath || file.name);
    }

    return showSpinnerDuring(
        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(res => res.json()).then(json => {
            if (!json.success) throw new Error(json.message || "Upload failed");
            return json;
        })
    );
}

// DnD events
dropzone.addEventListener('dragover', e => {
    e.preventDefault();
    dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('dragover');
});

dropzone.addEventListener('drop', e => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    if (e.dataTransfer.items) {
        const items = [...e.dataTransfer.items];
        const entries = items
            .map(item => item.webkitGetAsEntry?.())
            .filter(Boolean);
        if (entries.some(entry => entry.isDirectory)) {
            // Если папка, используем input fallback
            input.webkitdirectory = true;
            input.click();
        } else {
            uploadFileList(e.dataTransfer.files);
        }
    } else {
        uploadFileList(e.dataTransfer.files);
    }
});

// Клик по зоне — откроет файловый диалог
dropzone.addEventListener('click', () => {
    input.webkitdirectory = true;
    input.click();
});

input.addEventListener('change', () => {
    if (input.files.length > 0) {
        uploadFileList(input.files);
        input.value = "";
    }
});
