function updatePCStatus() {
    fetch('/pc_status')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const pcStatusElement = document.getElementById('pc-status-text');
                const pcAppsElement = document.getElementById('pc-apps');

                const pcStatusText = data.info.pc_status === '0' ? '活着' : '寄了';
                pcStatusElement.textContent = pcStatusText;

                pcAppsElement.textContent = data.info.pcapp_name.join(', ');
            }
        })
        .catch(error => console.error('Error fetching PC status:', error));
}

function updateMobileStatus() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const mobileStatusElement = document.getElementById('mobile-status-text');
                const mobileAppsElement = document.getElementById('mobile-apps');

                const mobileStatusText = data.info.mobile_status === '0' ? '活着' : '寄了';
                mobileStatusElement.textContent = mobileStatusText;

                mobileAppsElement.textContent = data.info.app_name.join(', ');
            }
        })
        .catch(error => console.error('Error fetching mobile status:', error));
}

function update() {
    updatePCStatus();
    updateMobileStatus();
}

// 首次获取数据
update();

// 每5秒更新一次数据
setInterval(update, 5000);