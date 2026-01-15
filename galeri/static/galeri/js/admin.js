// Admin Panel JavaScript Fonksiyonları

// Marka seçildiğinde modelleri yükle (Araç Ekle Sayfası)
document.addEventListener('DOMContentLoaded', function () {
    const markaSelect = document.getElementById('marka_id');
    const modelSelect = document.getElementById('model_id');

    if (markaSelect && modelSelect) {
        markaSelect.addEventListener('change', function () {
            const markaId = this.value;

            // Model select'i temizle
            modelSelect.innerHTML = '<option value="">Model Seçin</option>';

            if (markaId) {
                // AJAX ile modelleri yükle
                fetch(`/api/modeller/${markaId}/`)
                    .then(response => response.json())
                    .then(data => {
                        modelSelect.disabled = false;

                        if (data.modeller && data.modeller.length > 0) {
                            data.modeller.forEach(model => {
                                const option = document.createElement('option');
                                option.value = model.id;
                                option.textContent = model.ad;
                                modelSelect.appendChild(option);
                            });
                        } else {
                            modelSelect.innerHTML = '<option value="">Bu markaya ait model bulunamadı</option>';
                        }
                    })
                    .catch(error => {
                        console.error('Modeller yüklenirken hata:', error);
                        modelSelect.innerHTML = '<option value="">Modeller yüklenemedi</option>';
                    });
            } else {
                modelSelect.disabled = true;
                modelSelect.innerHTML = '<option value="">Önce Marka Seçin</option>';
            }
        });
    }

    // Satış fiyatı girildiğinde "Satıldı" checkbox'ını otomatik işaretle
    const satisFiyatInput = document.getElementById('satis_fiyat');
    const satildiMiCheckbox = document.getElementById('satildi_mi') || document.querySelector('input[name="satildi_mi"]');

    if (satisFiyatInput && satildiMiCheckbox) {
        satisFiyatInput.addEventListener('input', function () {
            if (this.value && parseFloat(this.value) > 0) {
                satildiMiCheckbox.checked = true;
            } else {
                satildiMiCheckbox.checked = false;
            }
        });
    }
});

// Fotoğraf silme fonksiyonu (Araç Düzenle Sayfası)
function silFoto(fotoId, url) {
    if (confirm('Bu fotoğrafı silmek istediğinizden emin misiniz?')) {
        const form = document.getElementById('foto-sil-form');
        form.action = url;
        form.submit();
    }
}
