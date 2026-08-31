let map;
let markers = [];
let currentJobs = [];
let currentJobType = '全部';

function initMap() {
    // 初始化地圖
    map = L.map('taiwanMap').setView([23.5, 121], 7);
    
    // 添加地圖圖層
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // 初始化職缺選擇器事件
    const jobTypeSelect = document.getElementById('jobTypeSelect');
    jobTypeSelect.addEventListener('change', function(e) {
        currentJobType = e.target.value;
        updateMap();
    });
    
    // 初始載入資料
    updateMap();
}

function createCustomIcon(count) {
    return L.divIcon({
        className: 'custom-div-icon',
        html: `
            <div class="marker-content">
                <i class="bi bi-geo-alt-fill"></i>
                <div class="job-count">${count}</div>
                <div class="pulse"></div>
            </div>
        `,
        iconSize: [40, 40],
        iconAnchor: [20, 40],
        popupAnchor: [0, -20]
    });
}

function updateMap() {
    const loadingElement = document.getElementById('loading');
    loadingElement.style.display = 'block';
    
    fetch(`/area_analysis/get_jobs/?job_type=${currentJobType}`)
        .then(response => response.json())
        .then(data => {
            currentJobs = data.jobs;
            
            // 更新總職缺數和標題
            updateHeader(data.total_jobs);
            
            // 清除現有標記
            clearMarkers();
            
            // 添加新的標記
            addMarkers(data.area_counts);
            
            loadingElement.style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            loadingElement.style.display = 'none';
        });
}

function updateHeader(totalJobs) {
    const totalJobsElement = document.getElementById('totalJobs');
    const jobTypeText = currentJobType === '全部' ? '所有職缺' : currentJobType;
    totalJobsElement.innerHTML = `
        <div class="total-jobs-header">
            <h5>${jobTypeText}</h5>
            <div class="total-count">總職缺數：${totalJobs}</div>
        </div>
    `;
}

function clearMarkers() {
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
}

function addMarkers(areaCounts) {
    areaCounts.forEach(area => {
        const marker = L.marker([area.lat, area.lng], {
            icon: createCustomIcon(area.count)
        });
        
        // 添加彈出視窗
        marker.bindPopup(createPopupContent(area));
        
        // 添加點擊事件
        marker.on('click', () => {
            showAreaJobs(area.area);
            marker.openPopup();
        });
        
        marker.addTo(map);
        markers.push(marker);
    });
}

function createPopupContent(area) {
    return `
        <div class="popup-content">
            <h6>${area.area}</h6>
            <p>職缺數：${area.count}</p>
            <button onclick="showAreaJobs('${area.area}')" 
                    class="btn btn-sm btn-primary">
                查看職缺詳情
            </button>
        </div>
    `;
}

function showAreaJobs(area) {
    const areaJobs = currentJobs.filter(job => job.area.includes(area));
    updateJobDetails(areaJobs, area);
}

function updateJobDetails(jobs, areaName) {
    const accordion = document.getElementById('jobAccordion');
    const title = document.getElementById('jobListTitle');
    
    // 更新標題
    title.textContent = `${areaName} - ${jobs.length} 個職缺`;
    
    if (jobs.length === 0) {
        accordion.innerHTML = '<div class="no-jobs">此地區無職缺</div>';
        return;
    }
    
    // 更新職缺列表
    accordion.innerHTML = jobs.map((job, index) => `
        <div class="accordion-item">
            <h2 class="accordion-header" id="heading${index}">
                <button class="accordion-button collapsed" type="button" 
                        data-bs-toggle="collapse" 
                        data-bs-target="#collapse${index}">
                    <div class="job-header">
                        <div class="job-title">${job.header}</div>
                        <div class="job-area">${job.area}</div>
                    </div>
                </button>
            </h2>
            <div id="collapse${index}" 
                 class="accordion-collapse collapse" 
                 data-bs-parent="#jobAccordion">
                <div class="accordion-body">
                    <div class="job-detail">
                        <p><strong>工作內容：</strong>${job.jobDetail}</p>
                        <p><strong>薪資：</strong>${job.salary}</p>
                        <p><strong>工作經驗：</strong>${job.workExp}</p>
                        <p><strong>學歷要求：</strong>${job.edu}</p>
                        <p><strong>工具：</strong>${job.tool}</p>
                        <p><strong>日期：</strong>${job.date}</p>
                        <a href="${job.link}" target="_blank" 
                           class="btn btn-primary">查看完整職缺</a>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
    
    // 平滑捲動到職缺列表
    document.querySelector('.job-details-container').scrollIntoView({ 
        behavior: 'smooth' 
    });
}

// 當頁面載入完成後初始化
document.addEventListener('DOMContentLoaded', initMap);