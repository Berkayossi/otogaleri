/**
 * Raporlar UI Functions
 * Hızlı filtre, tab geçişi ve diğer UI işlemleri
 */

// Hızlı filtreleme fonksiyonu
window.setQuickFilter = function (filterType) {
    var now = new Date();
    var currentYear = now.getFullYear();
    var currentMonth = now.getMonth() + 1;

    var baslangicYil, baslangicAy, bitisYil, bitisAy;

    switch (filterType) {
        case 'bu_ay':
            baslangicYil = currentYear;
            baslangicAy = currentMonth;
            bitisYil = currentYear;
            bitisAy = currentMonth;
            break;
        case 'gecen_ay':
            var lastMonth = new Date(currentYear, currentMonth - 2, 1);
            baslangicYil = lastMonth.getFullYear();
            baslangicAy = lastMonth.getMonth() + 1;
            bitisYil = lastMonth.getFullYear();
            bitisAy = lastMonth.getMonth() + 1;
            break;
        case 'bu_yil':
            baslangicYil = currentYear;
            baslangicAy = 0;
            bitisYil = currentYear;
            bitisAy = 0;
            break;
        case 'gecen_yil':
            baslangicYil = currentYear - 1;
            baslangicAy = 0;
            bitisYil = currentYear - 1;
            bitisAy = 0;
            break;
        case 'son_3_ay':
            var threeMonthsAgo = new Date(currentYear, currentMonth - 3, 1);
            baslangicYil = threeMonthsAgo.getFullYear();
            baslangicAy = threeMonthsAgo.getMonth() + 1;
            bitisYil = currentYear;
            bitisAy = currentMonth;
            break;
        case 'son_6_ay':
            var sixMonthsAgo = new Date(currentYear, currentMonth - 6, 1);
            baslangicYil = sixMonthsAgo.getFullYear();
            baslangicAy = sixMonthsAgo.getMonth() + 1;
            bitisYil = currentYear;
            bitisAy = currentMonth;
            break;
        case 'tumu':
            baslangicYil = 2020;
            baslangicAy = 0;
            bitisYil = currentYear;
            bitisAy = 0;
            break;
        default:
            return;
    }

    document.getElementById('baslangic_yil').value = baslangicYil;
    document.getElementById('baslangic_ay').value = baslangicAy;
    document.getElementById('bitis_yil').value = bitisYil;
    document.getElementById('bitis_ay').value = bitisAy;
    document.getElementById('tarihFiltreForm').submit();
};

// Filtre sıfırlama fonksiyonu
window.resetFilter = function () {
    var now = new Date();
    var currentYear = now.getFullYear();
    document.getElementById('baslangic_yil').value = currentYear;
    document.getElementById('baslangic_ay').value = 0;
    document.getElementById('bitis_yil').value = currentYear;
    document.getElementById('bitis_ay').value = 0;
    document.getElementById('tarihFiltreForm').submit();
};

// Tab değiştirme fonksiyonu
window.showTab = function (tabName) {
    document.querySelectorAll('.tab-content').forEach(function (tab) {
        tab.classList.add('hidden');
    });
    document.querySelectorAll('.tab-button').forEach(function (btn) {
        btn.classList.remove('active');
    });
    var tabElement = document.getElementById('tab-' + tabName);
    if (tabElement) {
        tabElement.classList.remove('hidden');
    }
    var btnElement = document.querySelector('[data-tab="' + tabName + '"]');
    if (btnElement) {
        btnElement.classList.add('active');
    }
};
