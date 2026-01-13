let selectedImageFile = null;     // выбранная пользователем картинка
let lastFilePath = null;          // путь к последнему QR
let isGenerating = false;         // защита от двойного клика

// ---------------- Цветовые поля ----------------
function applyColor(inputId, colorBoxId) {
    const colorInput = document.getElementById(inputId);
    const colorBox = document.getElementById(colorBoxId);

    colorInput.addEventListener('input', function () {
        const colorValue = this.value;

        const temp = document.createElement('div');
        temp.style.color = 'invalid';
        temp.style.color = colorValue;

        if (temp.style.color !== 'invalid') {
            colorBox.style.backgroundColor = colorValue;
            colorInput.style.borderColor = '#ddd';
        } else {
            colorInput.style.borderColor = '#e74c3c';
        }
    });
}

applyColor('foregroundInput', 'colorBox1');
applyColor('backgroundInput', 'colorBox2');

// ---------------- Кнопка фото ----------------
const fotoBtn = document.querySelector('.button_foto');
const imageInput = document.getElementById('bgImageInput');

fotoBtn.addEventListener('click', () => {
    imageInput.click();
});

imageInput.addEventListener('change', function () {
    if (this.files && this.files[0]) {
        selectedImageFile = this.files[0];
        fotoBtn.textContent = '✓';
        fotoBtn.style.background = '#2ecc71';
    }
});

// ---------------- Тень ----------------
const shadowToggle = document.getElementById('shadowToggle');
const shadowColorContainer = document.getElementById('shadowColorContainer');

function updateShadowColorVisibility() {
    shadowColorContainer.style.display = shadowToggle.checked ? 'block' : 'none';
}

shadowToggle.addEventListener('change', updateShadowColorVisibility);
updateShadowColorVisibility();

// ---------------- Отправка QR ----------------
document.getElementById('sendBtn').addEventListener('click', function () {

    if (isGenerating) return;
    isGenerating = true;

    const url = document.getElementById('urlInput').value;
    if (!url) {
        showMessage('Пожалуйста, введите URL-адрес', 'error');
        isGenerating = false;
        return;
    }

    const formData = new FormData();
    formData.append('url', url);
    formData.append(
        'foregroundColor',
        document.getElementById('foregroundInput').value || '#000000'
    );
    formData.append(
        'backgroundColor',
        document.getElementById('backgroundInput').value || ''
    );

    if (selectedImageFile) {
        formData.append('backgroundImage', selectedImageFile);
    }

    formData.append('shadowEnabled', shadowToggle.checked ? 'on' : 'off');
    formData.append(
        'shadowColor',
        document.getElementById('shadowColor').value || '#000000'
    );

    fetch('/make_qr', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(result => {
        if (result.status === "done") {
            lastFilePath = result.file;
            const qrImage = document.getElementById('qrImage');
            qrImage.src = result.file + '?t=' + Date.now();
            qrImage.style.display = 'block';
        } else {
            showMessage('Ошибка при создании QR', 'error');
        }
    })
    .catch(err => {
        console.error(err);
        showMessage('Ошибка при отправке запроса', 'error');
    })
    .finally(() => {
        isGenerating = false;
    });
});

// ---------------- Скачать QR ----------------
document.querySelector('.button_down').addEventListener('click', function () {
    if (lastFilePath) {
        window.location.href = `/download?file=${encodeURIComponent(lastFilePath)}`;
    } else {
        showMessage('Сначала создайте QR-код', 'error');
    }
});
