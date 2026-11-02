/**
 * AGRISENSE - Intelligent Crop Management & Decision Support System
 * Core Frontend Application Logic
 */

const AppState = {
  activeView: 'overview',
  location: {
    name: 'Central Agriculture Zone (Detecting...)',
    latitude: 21.1458,
    longitude: 79.0882
  },
  weather: null,
  lastPrediction: null,
  chatHistory: [],
  cropsCatalog: [],
  charts: {}
};

// ==========================================================================
// Initialization & Lifecycle
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initRangeSliders();
  initGeolocationAndWeather();
  initChatDrawer();
  loadCropsLibrary();
  loadFarmingHistory();
  loadMLMetrics();
});

// ==========================================================================
// Navigation & Views
// ==========================================================================
function initNavigation() {
  const navItems = document.querySelectorAll('.nav-item[data-view]');
  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const view = item.getAttribute('data-view');
      switchView(view);
    });
  });

  const menuToggle = document.getElementById('menuToggle');
  const sidebar = document.getElementById('sidebar');
  if (menuToggle && sidebar) {
    menuToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });
  }
}

function switchView(viewName) {
  AppState.activeView = viewName;

  // Update nav item active states
  document.querySelectorAll('.nav-item').forEach(el => {
    el.classList.toggle('active', el.getAttribute('data-view') === viewName);
  });

  // Update view sections
  document.querySelectorAll('.view-section').forEach(sec => {
    sec.classList.toggle('active', sec.id === `view-${viewName}`);
  });

  // Update title
  const titleMap = {
    overview: { title: 'Executive Farm Dashboard', sub: 'Holistic agricultural intelligence and field operations overview' },
    recommendation: { title: 'Crop Recommendation Engine', sub: 'Machine learning agronomic crop suitability prediction' },
    soil: { title: 'Soil Health & Fertility Diagnostics', sub: 'NPK macronutrient balance and pH remediation analysis' },
    weather: { title: 'Weather Intelligence Center', sub: 'Real-time hyper-local agrometeorological forecast and alerts' },
    irrigation: { title: 'Irrigation & Moisture Advisor', sub: 'Rule-based crop water budgeting and scheduling' },
    fertilizer: { title: 'Fertilizer & Nutrient Guidance', sub: 'Targeted organic, mineral, and biofertilizer management' },
    library: { title: 'Crop Information Library', sub: 'Comprehensive agronomic catalog of 22 cultivated crops' },
    comparison: { title: 'Crop Suitability Comparison', sub: 'Multi-crop parameter analysis and radar benchmarking' },
    calendar: { title: 'Crop Calendar & Phenology', sub: 'Growth stage timelines and field operations schedule' },
    history: { title: 'Farming Logs & Historical Records', sub: 'Persistent SQLite field observations and soil logs' },
    ml: { title: 'Machine Learning Performance Center', sub: 'Verified multiclass model evaluation metrics and confusion matrix' },
    chat: { title: 'AgriSense AI Agronomic Assistant', sub: 'Real Google Gemini generative intelligence with farm context' }
  };

  const meta = titleMap[viewName] || { title: 'AgriSense System', sub: 'Decision Support System' };
  document.getElementById('topbarPageTitle').textContent = meta.title;
  document.getElementById('topbarPageSubtitle').textContent = meta.sub;

  // Trigger view specific re-render/refresh
  if (viewName === 'comparison') {
    runCropComparison();
  } else if (viewName === 'ml') {
    loadMLMetrics();
  } else if (viewName === 'history') {
    loadFarmingHistory();
  } else if (viewName === 'calendar') {
    loadCalendarView();
  }

  // Close mobile sidebar if open
  const sidebar = document.getElementById('sidebar');
  if (sidebar && window.innerWidth <= 768) {
    sidebar.classList.remove('open');
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ==========================================================================
// Range Sliders Synchronizer
// ==========================================================================
function initRangeSliders() {
  const sliders = [
    { range: 'rangeN', num: 'inputN', val: 'valN', unit: 'kg/ha' },
    { range: 'rangeP', num: 'inputP', val: 'valP', unit: 'kg/ha' },
    { range: 'rangeK', num: 'inputK', val: 'valK', unit: 'kg/ha' },
    { range: 'rangeTemp', num: 'inputTemp', val: 'valTemp', unit: '°C' },
    { range: 'rangeHumid', num: 'inputHumid', val: 'valHumid', unit: '%' },
    { range: 'rangePH', num: 'inputPH', val: 'valPH', unit: 'pH' },
    { range: 'rangeRain', num: 'inputRain', val: 'valRain', unit: 'mm' }
  ];

  sliders.forEach(s => {
    const rEl = document.getElementById(s.range);
    const nEl = document.getElementById(s.num);
    const vEl = document.getElementById(s.val);

    if (rEl && nEl) {
      rEl.addEventListener('input', (e) => {
        nEl.value = e.target.value;
        if (vEl) vEl.textContent = `${e.target.value} ${s.unit}`;
      });
      nEl.addEventListener('input', (e) => {
        rEl.value = e.target.value;
        if (vEl) vEl.textContent = `${e.target.value} ${s.unit}`;
      });
    }
  });
}

// Auto-fill weather inputs into Recommendation form
function autoFillWeatherIntoPrediction() {
  if (!AppState.weather || !AppState.weather.current) {
    showToast('Weather data not loaded yet. Please wait or set location.', 'warning');
    return;
  }
  const curr = AppState.weather.current;
  const temp = Math.round(curr.temperature || 25);
  const humid = Math.round(curr.humidity || 70);

  const tRange = document.getElementById('rangeTemp');
  const tNum = document.getElementById('inputTemp');
  const tVal = document.getElementById('valTemp');
  if (tRange && tNum) {
    tRange.value = temp;
    tNum.value = temp;
    if (tVal) tVal.textContent = `${temp} °C`;
  }

  const hRange = document.getElementById('rangeHumid');
  const hNum = document.getElementById('inputHumid');
  const hVal = document.getElementById('valHumid');
  if (hRange && hNum) {
    hRange.value = humid;
    hNum.value = humid;
    if (hVal) hVal.textContent = `${humid} %`;
  }

  showToast(`Auto-filled ambient temperature (${temp}°C) and humidity (${humid}%)!`, 'success');
}

// ==========================================================================
// Geolocation & Weather
// ==========================================================================
function initGeolocationAndWeather() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;
        AppState.location.latitude = lat;
        AppState.location.longitude = lon;
        fetchWeather(lat, lon);
      },
      (err) => {
        console.warn('Geolocation initial request skipped or unavailable:', err.message);
        // Fallback to default central agricultural location
        fetchWeather(AppState.location.latitude, AppState.location.longitude);
      },
      { timeout: 8000 }
    );
  } else {
    fetchWeather(AppState.location.latitude, AppState.location.longitude);
  }

  // Location search modal handling
  const locBtn = document.getElementById('topbarLocationBtn');
  if (locBtn) {
    locBtn.addEventListener('click', () => openModal('locationModal'));
  }

  const searchInput = document.getElementById('locSearchInput');
  let debounceTimer;
  if (searchInput) {
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        triggerManualSearch();
      }
    });

    searchInput.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      const query = e.target.value.trim();
      if (query.length < 2) {
        document.getElementById('locSearchResults').innerHTML = '';
        return;
      }
      debounceTimer = setTimeout(() => searchLocationQuery(query), 350);
    });
  }
}

function triggerBrowserGPS() {
  const btn = document.getElementById('btnDetectGPS');
  if (btn) btn.innerHTML = '<span class="status-dot"></span> Requesting GPS Coordinates...';

  if (!navigator.geolocation) {
    showToast('Geolocation is not supported by your browser.', 'warning');
    if (btn) btn.innerHTML = 'Detect My Current GPS Location';
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const lat = pos.coords.latitude;
      const lon = pos.coords.longitude;
      AppState.location.latitude = lat;
      AppState.location.longitude = lon;
      closeModal('locationModal');
      fetchWeather(lat, lon);
      showToast('GPS Location detected successfully!', 'success');
      if (btn) btn.innerHTML = 'Detect My Current GPS Location';
    },
    (err) => {
      console.warn('Geolocation permission error:', err.message);
      let msg = 'Could not retrieve GPS location.';
      if (err.code === 1) {
        msg = 'Location permission blocked. If using Brave or Chrome, click the shield/lock icon in your address bar to allow location, or choose a city below.';
      } else if (err.code === 2) {
        msg = 'GPS Position unavailable. Please select your city from the list.';
      } else if (err.code === 3) {
        msg = 'Location request timed out. Please select your city manually.';
      }
      showToast(msg, 'warning');
      if (btn) btn.innerHTML = 'Detect My Current GPS Location';
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
  );
}

function triggerManualSearch() {
  const input = document.getElementById('locSearchInput');
  if (input && input.value.trim().length >= 2) {
    searchLocationQuery(input.value.trim());
  } else {
    showToast('Please type at least 2 characters to search.', 'info');
  }
}

async function searchLocationQuery(query) {
  const container = document.getElementById('locSearchResults');
  container.innerHTML = '<div style="padding: 0.75rem; color: #64748b; font-size: 0.82rem;">Searching locations...</div>';
  try {
    const res = await fetch(`/api/geocode?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    if (data.success && data.results.length > 0) {
      container.innerHTML = data.results.map(r => `
        <div class="loc-search-item" style="padding: 0.65rem 0.85rem; border-bottom: 1px solid #f1f5f9; display: flex; align-items: center; gap: 0.65rem; cursor: pointer;" onclick="selectSearchedLocation(${r.latitude}, ${r.longitude}, '${escapeHtml(r.display_name)}')">
          <svg style="width: 16px; height: 16px; color: #16a34a; flex-shrink: 0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          <div>
            <strong>${escapeHtml(r.name)}</strong>
            <div style="font-size: 0.72rem; color: #64748b;">${escapeHtml(r.display_name)}</div>
          </div>
        </div>
      `).join('');
    } else {
      container.innerHTML = '<div style="padding: 0.75rem; color: #94a3b8; font-size: 0.82rem;">No matching cities or districts found.</div>';
    }
  } catch (err) {
    container.innerHTML = '<div style="padding: 0.75rem; color: #ef4444; font-size: 0.82rem;">Error searching location.</div>';
  }
}

function selectSearchedLocation(lat, lon, name) {
  closeModal('locationModal');
  AppState.location = { latitude: lat, longitude: lon, name: name };

  // Immediately update UI labels
  const locPill = document.getElementById('topbarLocationText');
  if (locPill) locPill.textContent = name;
  const wLoc = document.getElementById('weatherViewLocation');
  if (wLoc) wLoc.textContent = name;

  // Show loading indicator in weather pill
  const weatherPill = document.getElementById('topbarWeatherPill');
  if (weatherPill) {
    weatherPill.innerHTML = `
      <span class="weather-pill-icon">⏳</span>
      <span class="weather-pill-temp">Updating...</span>
    `;
  }

  fetchWeather(lat, lon, name);
  showToast(`Location set to: ${name}`, 'success');
}

async function fetchWeather(lat, lon, locName = null) {
  const url = `/api/weather?lat=${lat}&lon=${lon}${locName ? `&name=${encodeURIComponent(locName)}` : ''}`;
  try {
    const res = await fetch(url);
    const data = await res.json();
    if (data.success) {
      AppState.weather = data;
      AppState.location.name = data.location.name;
      AppState.location.latitude = data.location.latitude;
      AppState.location.longitude = data.location.longitude;
      updateWeatherUI(data);
    } else {
      console.warn('Weather fetch warning:', data.error);
    }
  } catch (e) {
    console.error('Failed to load weather:', e);
  }
}

function updateWeatherUI(data) {
  const loc = data.location;
  const curr = data.current;

  // Topbar Pill
  const locPillText = document.getElementById('topbarLocationText');
  if (locPillText) locPillText.textContent = loc.name;

  const weatherPill = document.getElementById('topbarWeatherPill');
  if (weatherPill) {
    weatherPill.innerHTML = `
      <span class="weather-pill-icon">${getWeatherEmoji(curr.condition)}</span>
      <span class="weather-pill-temp">${Math.round(curr.temperature)}°C</span>
      <span style="font-size: 0.75rem; color: #475569;">${curr.condition}</span>
    `;
  }

  // Overview Weather Card
  const ovTemp = document.getElementById('ovWeatherTemp');
  if (ovTemp) ovTemp.textContent = `${Math.round(curr.temperature)}°C`;
  const ovCond = document.getElementById('ovWeatherCond');
  if (ovCond) ovCond.textContent = curr.condition;
  const ovHumid = document.getElementById('ovWeatherHumid');
  if (ovHumid) ovHumid.textContent = `${curr.humidity}%`;
  const ovWind = document.getElementById('ovWeatherWind');
  if (ovWind) ovWind.textContent = `${curr.wind_speed} km/h`;
  const ovRain = document.getElementById('ovWeatherRain');
  if (ovRain) ovRain.textContent = `${curr.precipitation} mm`;

  // Dedicated Weather Intelligence View
  const wViewLoc = document.getElementById('weatherViewLocation');
  if (wViewLoc) wViewLoc.textContent = loc.name;
  const wViewTemp = document.getElementById('weatherViewTemp');
  if (wViewTemp) wViewTemp.textContent = `${curr.temperature}°C`;
  const wViewCond = document.getElementById('weatherViewCond');
  if (wViewCond) wViewCond.textContent = curr.condition;
  const wViewApparent = document.getElementById('weatherViewApparent');
  if (wViewApparent) wViewApparent.textContent = `${curr.apparent_temperature}°C`;
  const wViewHumidity = document.getElementById('weatherViewHumidity');
  if (wViewHumidity) wViewHumidity.textContent = `${curr.humidity}%`;
  const wViewWind = document.getElementById('weatherViewWind');
  if (wViewWind) wViewWind.textContent = `${curr.wind_speed} km/h`;
  const wViewPrecip = document.getElementById('weatherViewPrecip');
  if (wViewPrecip) wViewPrecip.textContent = `${curr.precipitation} mm`;
  const wViewUpdated = document.getElementById('weatherViewUpdated');
  if (wViewUpdated) wViewUpdated.textContent = new Date(curr.last_updated).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  // Render 7-day forecast row
  const forecastRow = document.getElementById('weatherForecastCardsRow');
  if (forecastRow && data.daily_forecast) {
    forecastRow.innerHTML = data.daily_forecast.map((d, idx) => `
      <div class="forecast-day-card ${idx === 0 ? 'today' : ''}">
        <div class="forecast-day-name">${idx === 0 ? 'Today' : d.day_name}</div>
        <div class="forecast-day-date">${d.date_formatted}</div>
        <div class="forecast-day-icon">${getWeatherEmoji(d.condition)}</div>
        <div class="forecast-day-temps">${Math.round(d.max_temp)}° <span class="forecast-day-low">${Math.round(d.min_temp)}°</span></div>
        <div class="forecast-day-rain">🌧 ${d.rain_prob}%</div>
        <div style="font-size: 0.68rem; color: #64748b; margin-top: 0.25rem;">${d.condition}</div>
      </div>
    `).join('');
  }

  // Render Agricultural Alerts
  const alertsContainer = document.getElementById('weatherAlertsContainer');
  if (alertsContainer) {
    if (data.alerts && data.alerts.length > 0) {
      alertsContainer.innerHTML = data.alerts.map(a => `
        <div class="alert-box ${a.level === 'danger' ? 'danger' : (a.level === 'warning' ? 'warning' : 'info')}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          <div>
            <strong>${escapeHtml(a.title)}:</strong> ${escapeHtml(a.message)}
          </div>
        </div>
      `).join('');
    } else {
      alertsContainer.innerHTML = `
        <div class="alert-box info">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
          <div><strong>Favorable Conditions:</strong> No extreme weather alerts active. Temperature, humidity, and rainfall are currently within normal crop growth parameters.</div>
        </div>
      `;
    }
  }

  // Render hourly trend chart
  renderHourlyWeatherChart(data.hourly_trend);
}

function renderHourlyWeatherChart(hourlyData) {
  if (!hourlyData || hourlyData.length === 0) return;
  const ctx = document.getElementById('weatherHourlyChart');
  if (!ctx) return;

  if (AppState.charts['weatherHourly']) {
    AppState.charts['weatherHourly'].destroy();
  }

  const labels = hourlyData.map(h => h.time);
  const temps = hourlyData.map(h => h.temp);
  const rainProb = hourlyData.map(h => h.rain_prob);

  AppState.charts['weatherHourly'] = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Temperature (°C)',
          data: temps,
          borderColor: '#15803d',
          backgroundColor: 'rgba(21, 128, 61, 0.08)',
          fill: true,
          tension: 0.35,
          yAxisID: 'y'
        },
        {
          label: 'Precipitation Prob (%)',
          data: rainProb,
          borderColor: '#2563eb',
          borderDash: [4, 4],
          tension: 0.2,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top' }
      },
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          title: { display: true, text: 'Temperature (°C)' }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          grid: { drawOnChartArea: false },
          title: { display: true, text: 'Rain Probability (%)' },
          min: 0,
          max: 100
        }
      }
    }
  });
}

function getWeatherEmoji(condition) {
  if (!condition) return '☀️';
  const c = condition.toLowerCase();
  if (c.includes('thunder') || c.includes('hail')) return '⛈️';
  if (c.includes('rain') || c.includes('drizzle') || c.includes('shower')) return '🌧️';
  if (c.includes('snow')) return '❄️';
  if (c.includes('cloud') || c.includes('overcast')) return '⛅';
  if (c.includes('fog') || c.includes('smog')) return '🌫️';
  return '☀️';
}

// ==========================================================================
// Feature 1: Crop Recommendation Engine
// ==========================================================================
async function submitCropRecommendation() {
  const btn = document.getElementById('btnPredictCrop');
  const resultCard = document.getElementById('predictionResultCard');
  const heroCropName = document.getElementById('recHeroCropName');
  const heroConfidence = document.getElementById('recHeroConfidence');
  const heroExplanation = document.getElementById('recHeroExplanation');
  const alternativesContainer = document.getElementById('recHeroAlternatives');
  const plotName = document.getElementById('recPlotName') ? document.getElementById('recPlotName').value : 'Plot Alpha';

  const payload = {
    field_name: plotName,
    N: parseFloat(document.getElementById('inputN').value),
    P: parseFloat(document.getElementById('inputP').value),
    K: parseFloat(document.getElementById('inputK').value),
    temperature: parseFloat(document.getElementById('inputTemp').value),
    humidity: parseFloat(document.getElementById('inputHumid').value),
    ph: parseFloat(document.getElementById('inputPH').value),
    rainfall: parseFloat(document.getElementById('inputRain').value),
    location_name: AppState.location.name,
    latitude: AppState.location.latitude,
    longitude: AppState.location.longitude,
    save_history: true
  };

  btn.disabled = true;
  btn.innerHTML = '<span class="status-dot"></span> Computing ML Recommendation...';

  try {
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (data.success) {
      AppState.lastPrediction = data;
      resultCard.style.display = 'block';

      heroCropName.textContent = data.recommended_crop;
      heroConfidence.textContent = `${data.confidence}%`;
      heroExplanation.textContent = data.explanation;

      // Alternatives
      if (data.alternatives && data.alternatives.length > 0) {
        alternativesContainer.innerHTML = data.alternatives.map(a => `
          <div class="alt-crop-pill">
            <span style="text-transform: capitalize; font-weight: 600;">${a.crop}</span>
            <span style="opacity: 0.8; font-size: 0.72rem;">${a.confidence}% fit</span>
          </div>
        `).join('');
      } else {
        alternativesContainer.innerHTML = '<span style="font-size: 0.8rem; opacity: 0.8;">No close alternatives for this profile.</span>';
      }

      // Update overview recommendation card
      const ovCrop = document.getElementById('ovLastRecCrop');
      if (ovCrop) ovCrop.textContent = data.recommended_crop.toUpperCase();
      const ovConf = document.getElementById('ovLastRecConf');
      if (ovConf) ovConf.textContent = `Confidence: ${data.confidence}%`;

      showToast(`Optimal Crop Identified: ${data.recommended_crop.toUpperCase()} (${data.confidence}%)`, 'success');

      // Scroll to result smoothly
      resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });

      // Refresh farming history table in background
      loadFarmingHistory();
    } else {
      const errorMsg = data.errors ? data.errors.join('<br>') : (data.error || 'Prediction failed');
      showToast(errorMsg, 'danger');
    }
  } catch (err) {
    showToast('Network error during crop prediction: ' + err.message, 'danger');
  } finally {
    btn.disabled = false;
    btn.innerHTML = `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
      Analyze & Recommend Crop
    `;
  }
}

// ==========================================================================
// Feature 2: Soil Health Analysis
// ==========================================================================
async function submitSoilAnalysis() {
  const n = parseFloat(document.getElementById('soilInputN').value);
  const p = parseFloat(document.getElementById('soilInputP').value);
  const k = parseFloat(document.getElementById('soilInputK').value);
  const ph = parseFloat(document.getElementById('soilInputPH').value);

  const btn = document.getElementById('btnAnalyzeSoil');
  btn.disabled = true;
  btn.innerHTML = 'Analyzing Soil Metrics...';

  try {
    const res = await fetch('/api/soil-health', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nitrogen: n, phosphorus: p, potassium: k, ph: ph })
    });
    const data = await res.json();

    if (data.success) {
      document.getElementById('soilResultsContainer').style.display = 'block';

      // Score
      document.getElementById('soilOverallScoreVal').textContent = `${data.overall_score}/100`;
      const badge = document.getElementById('soilOverallBadge');
      badge.textContent = data.overall_health;
      badge.className = `badge badge-${data.health_badge}`;

      // pH interpretation
      document.getElementById('soilPHStatus').textContent = data.ph_analysis.status;
      document.getElementById('soilPHImpact').textContent = data.ph_analysis.impact;
      document.getElementById('soilPHRemedy').textContent = data.ph_analysis.remedy;

      // Nutrients Breakdown
      const nNut = data.nutrients.N;
      const pNut = data.nutrients.P;
      const kNut = data.nutrients.K;

      document.getElementById('soilNStatus').innerHTML = `<span class="badge badge-${nNut.badge}">${nNut.status}</span>`;
      document.getElementById('soilNAdvice').textContent = nNut.advice;

      document.getElementById('soilPStatus').innerHTML = `<span class="badge badge-${pNut.badge}">${pNut.status}</span>`;
      document.getElementById('soilPAdvice').textContent = pNut.advice;

      document.getElementById('soilKStatus').innerHTML = `<span class="badge badge-${kNut.badge}">${kNut.status}</span>`;
      document.getElementById('soilKAdvice').textContent = kNut.advice;

      // Improvement Plan list
      const planList = document.getElementById('soilImprovementList');
      planList.innerHTML = data.improvement_plan.map(item => `
        <li style="margin-bottom: 0.65rem;">
          <strong style="color: #0f172a;">${escapeHtml(item.title)}:</strong>
          <span style="color: #475569;">${escapeHtml(item.detail)}</span>
        </li>
      `).join('');

      renderSoilBarChart(n, p, k);
      showToast('Soil Health Diagnostics Generated', 'success');
      document.getElementById('soilResultsContainer').scrollIntoView({ behavior: 'smooth' });
    } else {
      showToast(data.error || 'Failed to analyze soil.', 'danger');
    }
  } catch (err) {
    showToast('Soil analysis error: ' + err.message, 'danger');
  } finally {
    btn.disabled = false;
    btn.innerHTML = 'Evaluate Soil Health';
  }
}

function renderSoilBarChart(n, p, k) {
  const ctx = document.getElementById('soilNutrientsChart');
  if (!ctx) return;

  if (AppState.charts['soilBar']) {
    AppState.charts['soilBar'].destroy();
  }

  AppState.charts['soilBar'] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)'],
      datasets: [
        {
          label: 'Your Soil Test Value (kg/ha)',
          data: [n, p, k],
          backgroundColor: ['#16a34a', '#0284c7', '#d97706'],
          borderRadius: 6
        },
        {
          label: 'Optimal Agronomic Benchmark',
          data: [60, 45, 55],
          backgroundColor: 'rgba(148, 163, 184, 0.35)',
          borderRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: true, title: { display: true, text: 'kg/ha' } }
      }
    }
  });
}

// ==========================================================================
// Feature 4: Irrigation Advisor
// ==========================================================================
async function submitIrrigationCheck() {
  const cropId = document.getElementById('irrigCropSelect').value;
  const temp = parseFloat(document.getElementById('irrigTemp').value) || 25.0;
  const humid = parseFloat(document.getElementById('irrigHumid').value) || 60.0;
  const recentRain = parseFloat(document.getElementById('irrigRecentRain').value) || 0.0;
  const forecastRain = parseFloat(document.getElementById('irrigForecastRain').value) || 0.0;
  const soilType = document.getElementById('irrigSoilType').value;
  const surfaceState = document.getElementById('irrigSurfaceState').value;

  const btn = document.getElementById('btnCalculateIrrig');
  btn.disabled = true;

  try {
    const res = await fetch('/api/irrigation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        crop_id: cropId,
        temperature: temp,
        humidity: humid,
        recent_rainfall: recentRain,
        forecast_rain_48h: forecastRain,
        soil_type: soilType,
        surface_state: surfaceState
      })
    });
    const data = await res.json();

    if (data.success) {
      const container = document.getElementById('irrigResultCard');
      container.style.display = 'block';

      document.getElementById('irrigRecommendationText').textContent = data.recommendation;
      const pBadge = document.getElementById('irrigPriorityBadge');
      pBadge.textContent = `Priority: ${data.priority}`;
      pBadge.className = `badge badge-${data.priority_badge}`;

      document.getElementById('irrigActionText').textContent = data.action;
      document.getElementById('irrigEvapIndex').textContent = `${data.evaporative_demand_index} (VPD proxy)`;

      // Reasons list
      const reasonsList = document.getElementById('irrigReasonsList');
      reasonsList.innerHTML = data.reasons.map(r => `<li>${escapeHtml(r)}</li>`).join('');

      // Warnings
      const warnBox = document.getElementById('irrigWarningsBox');
      if (data.warnings && data.warnings.length > 0) {
        warnBox.style.display = 'block';
        warnBox.innerHTML = `<strong>Field Cautions:</strong><br>${data.warnings.map(w => `• ${escapeHtml(w)}`).join('<br>')}`;
      } else {
        warnBox.style.display = 'none';
      }

      document.getElementById('irrigTipText').textContent = data.best_practice;

      container.scrollIntoView({ behavior: 'smooth' });
    }
  } catch (err) {
    showToast('Failed to calculate irrigation: ' + err.message, 'danger');
  } finally {
    btn.disabled = false;
  }
}

// Auto-fill weather into irrigation form
function autoFillWeatherIntoIrrigation() {
  if (!AppState.weather || !AppState.weather.current) {
    showToast('Weather not available yet.', 'warning');
    return;
  }
  const curr = AppState.weather.current;
  const daily = AppState.weather.daily_forecast;

  document.getElementById('irrigTemp').value = Math.round(curr.temperature || 25);
  document.getElementById('irrigHumid').value = Math.round(curr.humidity || 60);
  document.getElementById('irrigRecentRain').value = curr.precipitation || 0;

  // Next 48h rain sum from daily
  let sum48h = 0;
  if (daily && daily.length >= 2) {
    sum48h = (daily[0].precipitation_sum || 0) + (daily[1].precipitation_sum || 0);
  }
  document.getElementById('irrigForecastRain').value = Math.round(sum48h * 10) / 10;

  showToast('Synchronized live weather parameters to irrigation advisor!', 'success');
}

// ==========================================================================
// Feature 6: Fertilizer Advisor
// ==========================================================================
async function submitFertilizerAdvisor() {
  const n = parseFloat(document.getElementById('fertInputN').value);
  const p = parseFloat(document.getElementById('fertInputP').value);
  const k = parseFloat(document.getElementById('fertInputK').value);
  const ph = parseFloat(document.getElementById('fertInputPH').value);
  const cropId = document.getElementById('fertCropSelect').value;

  const btn = document.getElementById('btnCalculateFert');
  btn.disabled = true;

  try {
    const res = await fetch('/api/fertilizer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nitrogen: n, phosphorus: p, potassium: k, ph: ph, crop_id: cropId })
    });
    const data = await res.json();

    if (data.success) {
      const container = document.getElementById('fertResultsContainer');
      container.style.display = 'block';

      // Diagnostics
      const diagContainer = document.getElementById('fertDiagnosticsList');
      diagContainer.innerHTML = data.diagnostics.map(d => `
        <div style="padding: 0.75rem; border-radius: 8px; background: #f8fafc; border: 1px solid #e2e8f0; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
          <div>
            <strong>${escapeHtml(d.nutrient)}:</strong> <span style="font-size: 0.85rem; color: #475569;">${escapeHtml(d.observation)}</span>
          </div>
          <span class="badge badge-${d.badge}">${d.status}</span>
        </div>
      `).join('');

      // Mineral fertilizers
      const chemContainer = document.getElementById('fertChemOptions');
      if (data.recommended_fertilizers.length > 0) {
        chemContainer.innerHTML = data.recommended_fertilizers.map(cat => `
          <div style="margin-bottom: 1rem;">
            <div style="font-weight: 700; color: #166534; font-size: 0.9rem; margin-bottom: 0.35rem;">${escapeHtml(cat.category)}</div>
            <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.5rem;">Strategy: ${escapeHtml(cat.application_strategy)}</div>
            <div style="display: grid; gap: 0.5rem;">
              ${cat.options.map(opt => `
                <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 0.6rem 0.85rem;">
                  <strong style="color: #0f172a;">${escapeHtml(opt.name)}</strong> (${escapeHtml(opt.composition)})
                  <div style="font-size: 0.78rem; color: #475569;">${escapeHtml(opt.notes)}</div>
                </div>
              `).join('')}
            </div>
          </div>
        `).join('');
      } else {
        chemContainer.innerHTML = '<div style="color: #16a34a; font-weight: 600;">Nutrient reserves are balanced. No heavy chemical supplementation needed.</div>';
      }

      // Biofertilizers
      const bioContainer = document.getElementById('fertBioOptions');
      bioContainer.innerHTML = data.biofertilizers.map(b => `
        <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 6px; padding: 0.65rem 0.85rem; margin-bottom: 0.5rem;">
          <strong style="color: #166534;">${escapeHtml(b.name)}</strong> <span style="font-size: 0.72rem; color: #64748b;">(${escapeHtml(b.strain)})</span>
          <div style="font-size: 0.8rem; color: #334155; margin-top: 0.2rem;">${escapeHtml(b.benefit)}</div>
        </div>
      `).join('');

      // Cautions
      const cautionsBox = document.getElementById('fertCautionsBox');
      if (data.cautions && data.cautions.length > 0) {
        cautionsBox.style.display = 'block';
        cautionsBox.innerHTML = `<strong>Nutrient Interactions & Soil Limits:</strong><br>${data.cautions.map(c => `• ${escapeHtml(c)}`).join('<br>')}`;
      } else {
        cautionsBox.style.display = 'none';
      }

      container.scrollIntoView({ behavior: 'smooth' });
    }
  } catch (err) {
    showToast('Fertilizer advisor error: ' + err.message, 'danger');
  } finally {
    btn.disabled = false;
  }
}

// ==========================================================================
// Feature 5: Crop Information Library
// ==========================================================================
async function loadCropsLibrary() {
  try {
    const res = await fetch('/api/crops');
    const data = await res.json();
    if (data.success) {
      AppState.cropsCatalog = data.crops;
      renderCropsGrid(data.crops);
      populateCropDropdowns(data.crops);
    }
  } catch (err) {
    console.error('Failed to load crop catalog:', err);
  }
}

function renderCropsGrid(crops) {
  const grid = document.getElementById('cropsCatalogGrid');
  if (!grid) return;

  if (crops.length === 0) {
    grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: #94a3b8;">No matching crops found in library.</div>';
    return;
  }

  grid.innerHTML = crops.map(c => `
    <div class="crop-card">
      <div>
        <div class="crop-card-top">
          <div>
            <div class="crop-card-name">${escapeHtml(c.name)}</div>
            <div class="crop-card-sci">${escapeHtml(c.scientific_name)} • ${escapeHtml(c.family)}</div>
          </div>
          <span class="badge badge-success">${escapeHtml(c.category)}</span>
        </div>

        <div class="crop-card-tags">
          <span class="badge badge-neutral">🗓 ${escapeHtml(c.season.split('(')[0])}</span>
          <span class="badge badge-neutral">⏱ ${escapeHtml(c.duration_days.split('(')[0])}</span>
          <span class="badge badge-neutral">💧 ${escapeHtml(c.water_requirement)}</span>
        </div>

        <p class="crop-card-desc">${escapeHtml(c.description.substring(0, 140))}...</p>
      </div>

      <div class="crop-card-footer">
        <span style="font-size: 0.72rem; color: #64748b;">pH: ${escapeHtml(c.optimal_ph)}</span>
        <button class="btn btn-outline-primary btn-sm" onclick="openCropDetailModal('${c.id}')">
          Full Agronomic Profile
        </button>
      </div>
    </div>
  `).join('');
}

function filterCropsCatalog() {
  const q = document.getElementById('cropSearchInput').value.toLowerCase().trim();
  const cat = document.getElementById('cropCategoryFilter').value;
  const season = document.getElementById('cropSeasonFilter').value;

  const filtered = AppState.cropsCatalog.filter(c => {
    let match = true;
    if (q) {
      const matchName = c.name.toLowerCase().includes(q) || c.scientific_name.toLowerCase().includes(q) || c.id.includes(q);
      if (!matchName) match = false;
    }
    if (cat !== 'all' && !c.category.toLowerCase().includes(cat.toLowerCase())) {
      match = false;
    }
    if (season !== 'all' && !c.season.toLowerCase().includes(season.toLowerCase())) {
      match = false;
    }
    return match;
  });

  renderCropsGrid(filtered);
}

function populateCropDropdowns(crops) {
  const selects = ['irrigCropSelect', 'fertCropSelect', 'calendarCropSelect'];
  selects.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.innerHTML = crops.map(c => `
        <option value="${c.id}" ${c.id === 'rice' ? 'selected' : ''}>${c.name} (${c.category})</option>
      `).join('');
    }
  });

  // Comparison checkboxes
  const compBox = document.getElementById('comparisonCheckboxes');
  if (compBox) {
    compBox.innerHTML = crops.map((c, idx) => `
      <label style="display: flex; align-items: center; gap: 0.4rem; font-size: 0.82rem; cursor: pointer;">
        <input type="checkbox" name="compCrop" value="${c.id}" ${idx < 3 ? 'checked' : ''} onchange="runCropComparison()">
        <span style="text-transform: capitalize;">${c.name}</span>
      </label>
    `).join('');
  }
}

function openCropDetailModal(cropId) {
  const crop = AppState.cropsCatalog.find(c => c.id === cropId);
  if (!crop) return;

  document.getElementById('modalCropTitle').textContent = crop.name;
  document.getElementById('modalCropScientific').textContent = `${crop.scientific_name} | Family: ${crop.family} | Category: ${crop.category}`;
  document.getElementById('modalCropDesc').textContent = crop.description;

  document.getElementById('modalCropSeason').textContent = crop.season;
  document.getElementById('modalCropDuration').textContent = crop.duration_days;
  document.getElementById('modalCropWater').textContent = `${crop.water_requirement} (${crop.rainfall_range})`;
  document.getElementById('modalCropSoil').textContent = crop.soil_type;
  document.getElementById('modalCropTemp').textContent = crop.optimal_temp;
  document.getElementById('modalCropPH').textContent = crop.optimal_ph;

  const tipsList = document.getElementById('modalCropTips');
  tipsList.innerHTML = crop.cultivation_tips.map(t => `<li style="margin-bottom: 0.4rem;">${escapeHtml(t)}</li>`).join('');

  const stagesList = document.getElementById('modalCropStages');
  stagesList.innerHTML = crop.stages.map(s => `
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.5rem 0.8rem; margin-bottom: 0.4rem;">
      <strong style="color: #166534;">${escapeHtml(s.stage)}</strong> <span style="font-size: 0.75rem; color: #64748b;">(${escapeHtml(s.days)})</span>
      <div style="font-size: 0.78rem; color: #475569;">${escapeHtml(s.desc)}</div>
    </div>
  `).join('');

  openModal('cropDetailModal');
}

// ==========================================================================
// Feature 7: Crop Suitability Comparison
// ==========================================================================
async function runCropComparison() {
  const checkboxes = document.querySelectorAll('input[name="compCrop"]:checked');
  const selectedCrops = Array.from(checkboxes).map(cb => cb.value);

  if (selectedCrops.length === 0) {
    showToast('Select at least one crop to compare.', 'warning');
    return;
  }

  // Get current farm params from recommendation form
  const params = {
    N: parseFloat(document.getElementById('inputN') ? document.getElementById('inputN').value : 50),
    P: parseFloat(document.getElementById('inputP') ? document.getElementById('inputP').value : 50),
    K: parseFloat(document.getElementById('inputK') ? document.getElementById('inputK').value : 50),
    temperature: parseFloat(document.getElementById('inputTemp') ? document.getElementById('inputTemp').value : 25),
    humidity: parseFloat(document.getElementById('inputHumid') ? document.getElementById('inputHumid').value : 70),
    ph: parseFloat(document.getElementById('inputPH') ? document.getElementById('inputPH').value : 6.5),
    rainfall: parseFloat(document.getElementById('inputRain') ? document.getElementById('inputRain').value : 100)
  };

  try {
    const res = await fetch('/api/compare', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ crop_ids: selectedCrops, farm_params: params })
    });
    const data = await res.json();

    if (data.success) {
      renderComparisonTable(data.crops);
      renderComparisonRadarChart(data.crops);
    }
  } catch (err) {
    console.error('Comparison error:', err);
  }
}

function renderComparisonTable(crops) {
  const tableBody = document.getElementById('comparisonTableBody');
  if (!tableBody) return;

  tableBody.innerHTML = crops.map(c => `
    <tr>
      <td><strong>${escapeHtml(c.name)}</strong></td>
      <td>
        <div style="font-size: 1.15rem; font-weight: 800; color: ${c.suitability_score > 75 ? '#16a34a' : (c.suitability_score > 50 ? '#d97706' : '#dc2626')};">
          ${c.suitability_score}%
        </div>
      </td>
      <td>${c.scores.climate}%</td>
      <td>${c.scores.water}%</td>
      <td>${c.scores.soil_ph}%</td>
      <td>${c.scores.nutrients}%</td>
      <td>${escapeHtml(c.duration)}</td>
      <td><span class="badge badge-neutral">${escapeHtml(c.water_requirement)}</span></td>
    </tr>
  `).join('');
}

function renderComparisonRadarChart(crops) {
  const ctx = document.getElementById('comparisonRadarChart');
  if (!ctx) return;

  if (AppState.charts['comparisonRadar']) {
    AppState.charts['comparisonRadar'].destroy();
  }

  const colors = [
    { border: '#16a34a', bg: 'rgba(22, 163, 74, 0.2)' },
    { border: '#2563eb', bg: 'rgba(37, 99, 235, 0.2)' },
    { border: '#d97706', bg: 'rgba(217, 119, 6, 0.2)' },
    { border: '#9333ea', bg: 'rgba(147, 51, 234, 0.2)' }
  ];

  const labels = ['Thermal Match', 'Humidity Match', 'Rainfall Match', 'Soil pH Match', 'NPK Balance'];

  const datasets = crops.slice(0, 4).map((c, idx) => ({
    label: c.name,
    data: c.radar_metrics.map(m => m.value),
    borderColor: colors[idx % colors.length].border,
    backgroundColor: colors[idx % colors.length].bg,
    borderWidth: 2
  }));

  AppState.charts['comparisonRadar'] = new Chart(ctx, {
    type: 'radar',
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          beginAtZero: true,
          max: 100,
          ticks: { stepSize: 20 }
        }
      }
    }
  });
}

// ==========================================================================
// Feature 8: Crop Calendar
// ==========================================================================
async function loadCalendarView() {
  const cropSelect = document.getElementById('calendarCropSelect');
  const cropId = cropSelect ? (cropSelect.value || 'rice') : 'rice';

  try {
    const res = await fetch(`/api/calendar/${cropId}`);
    const data = await res.json();

    if (data.success) {
      const cropNameEl = document.getElementById('calCropName');
      if (cropNameEl) cropNameEl.textContent = data.crop_name;

      const durEl = document.getElementById('calDuration');
      if (durEl) durEl.textContent = data.duration_days;

      const seasonEl = document.getElementById('calSeason');
      if (seasonEl) seasonEl.textContent = data.season;

      const sowingEl = document.getElementById('calSowingMonths');
      if (sowingEl && data.season_details) sowingEl.textContent = data.season_details.sowing_months;

      const activeEl = document.getElementById('calActiveMonths');
      if (activeEl && data.season_details) activeEl.textContent = data.season_details.active_months;

      const harvestEl = document.getElementById('calHarvestMonths');
      if (harvestEl && data.season_details) harvestEl.textContent = data.season_details.harvesting_months;

      // Render Stages
      const stagesContainer = document.getElementById('calStagesTimeline');
      if (stagesContainer && data.stages) {
        stagesContainer.innerHTML = data.stages.map((s, idx) => `
          <div style="display: flex; gap: 1rem; margin-bottom: 1.25rem;">
            <div style="display: flex; flex-direction: column; align-items: center;">
              <div style="width: 28px; height: 28px; border-radius: 50%; background: #16a34a; color: #fff; font-weight: 700; display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">
                ${idx + 1}
              </div>
              ${idx < data.stages.length - 1 ? '<div style="width: 2px; flex: 1; background: #cbd5e1; margin: 4px 0;"></div>' : ''}
            </div>
            <div style="flex: 1; padding-bottom: 0.5rem;">
              <div style="display: flex; justify-content: space-between; align-items: baseline;">
                <strong style="color: #0f172a; font-size: 0.95rem;">${escapeHtml(s.stage)}</strong>
                <span class="badge badge-neutral">${escapeHtml(s.days)}</span>
              </div>
              <p style="font-size: 0.82rem; color: #475569; margin-top: 0.25rem;">${escapeHtml(s.desc)}</p>
            </div>
          </div>
        `).join('');
      }

      // Operations
      const opsContainer = document.getElementById('calOperationsChecklist');
      if (opsContainer && data.operations) {
        opsContainer.innerHTML = data.operations.map(op => `
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.85rem 1rem; margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
              <strong style="color: #166534; font-size: 0.9rem;">${op.step}. ${escapeHtml(op.phase)}</strong>
              <span style="font-size: 0.75rem; color: #64748b;">${escapeHtml(op.timeframe)}</span>
            </div>
            <ul style="padding-left: 1.25rem; font-size: 0.8rem; color: #334155;">
              ${op.activities.map(act => `<li style="margin-bottom: 0.25rem;">${escapeHtml(act)}</li>`).join('')}
            </ul>
          </div>
        `).join('');
      }
    }
  } catch (err) {
    console.error('Calendar error:', err);
  }
}

// ==========================================================================
// Feature 9: Farming History
// ==========================================================================
async function loadFarmingHistory() {
  try {
    const res = await fetch('/api/history');
    const data = await res.json();
    if (data.success) {
      renderHistoryTable(data.records);
      updateHistorySummaryUI(data.summary);
    }
  } catch (err) {
    console.error('Failed to load history:', err);
  }
}

function updateHistorySummaryUI(summary) {
  if (!summary) return;
  const tot = document.getElementById('histTotalRecords');
  if (tot) tot.textContent = summary.total_records;

  const topCropEl = document.getElementById('histTopCrop');
  if (topCropEl && summary.top_crops && summary.top_crops.length > 0) {
    topCropEl.textContent = summary.top_crops[0].crop_recommended.toUpperCase();
  }

  const avgN = document.getElementById('histAvgN');
  if (avgN) avgN.textContent = `${summary.averages.n} kg/ha`;
  const avgP = document.getElementById('histAvgP');
  if (avgP) avgP.textContent = `${summary.averages.p} kg/ha`;
  const avgK = document.getElementById('histAvgK');
  if (avgK) avgK.textContent = `${summary.averages.k} kg/ha`;
  const avgPH = document.getElementById('histAvgPH');
  if (avgPH) avgPH.textContent = summary.averages.ph;
}

function renderHistoryTable(records) {
  const tbody = document.getElementById('historyTableBody');
  if (!tbody) return;

  if (records.length === 0) {
    tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 2rem; color: #94a3b8;">No historical farming records saved yet. Run a crop recommendation or log a record above.</td></tr>';
    return;
  }

  tbody.innerHTML = records.map(r => `
    <tr>
      <td style="font-size: 0.78rem; color: #64748b;">${escapeHtml(r.timestamp.substring(0, 16))}</td>
      <td><strong>${escapeHtml(r.field_name)}</strong><br><span style="font-size: 0.72rem; color: #64748b;">${escapeHtml(r.location_name || '')}</span></td>
      <td><span class="badge badge-success" style="font-size: 0.78rem;">${escapeHtml(r.crop_recommended.toUpperCase())}</span></td>
      <td><strong>${r.confidence ? r.confidence + '%' : 'N/A'}</strong></td>
      <td style="font-family: monospace; font-size: 0.78rem;">N:${r.nitrogen} P:${r.phosphorus} K:${r.potassium}</td>
      <td>${r.temperature}°C / ${r.humidity}%</td>
      <td style="max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${escapeHtml(r.notes || '')}">
        ${escapeHtml(r.notes || '-')}
      </td>
      <td>
        <button class="btn btn-secondary btn-sm" style="color: #dc2626; padding: 0.2rem 0.5rem;" onclick="deleteHistoryItem(${r.id})">
          Delete
        </button>
      </td>
    </tr>
  `).join('');
}

async function deleteHistoryItem(id) {
  if (!confirm('Are you sure you want to delete this farming record?')) return;
  try {
    const res = await fetch(`/api/history/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      showToast('Record deleted.', 'info');
      loadFarmingHistory();
    }
  } catch (e) {
    showToast('Failed to delete: ' + e.message, 'danger');
  }
}

// Manual History Log Modal
async function submitManualHistoryRecord() {
  const plotName = document.getElementById('logPlotName').value || 'Manual Plot';
  const crop = document.getElementById('logCrop').value || 'Wheat';
  const n = parseFloat(document.getElementById('logN').value) || 50;
  const p = parseFloat(document.getElementById('logP').value) || 50;
  const k = parseFloat(document.getElementById('logK').value) || 50;
  const ph = parseFloat(document.getElementById('logPH').value) || 6.5;
  const temp = parseFloat(document.getElementById('logTemp').value) || 25;
  const humid = parseFloat(document.getElementById('logHumid').value) || 60;
  const rain = parseFloat(document.getElementById('logRain').value) || 80;
  const notes = document.getElementById('logNotes').value || 'Field manual observation';

  const payload = {
    field_name: plotName,
    crop_recommended: crop,
    confidence: 100,
    nitrogen: n,
    phosphorus: p,
    potassium: k,
    ph: ph,
    temperature: temp,
    humidity: humid,
    rainfall: rain,
    location_name: AppState.location.name,
    latitude: AppState.location.latitude,
    longitude: AppState.location.longitude,
    notes: notes
  };

  try {
    const res = await fetch('/api/history', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      closeModal('manualLogModal');
      showToast('Field record logged successfully into SQLite database!', 'success');
      loadFarmingHistory();
    }
  } catch (e) {
    showToast('Failed to save log: ' + e.message, 'danger');
  }
}

// ==========================================================================
// Feature 10: Machine Learning Performance Center
// ==========================================================================
async function loadMLMetrics() {
  try {
    const res = await fetch('/api/ml-metrics');
    const data = await res.json();
    if (data.success) {
      renderMLMetricsUI(data.metrics);
    }
  } catch (err) {
    console.error('Failed to load ML metrics:', err);
  }
}

function renderMLMetricsUI(metrics) {
  const dsInfo = metrics.dataset_info;
  const models = metrics.models_comparison;

  document.getElementById('mlTotalSamples').textContent = dsInfo.total_samples.toLocaleString();
  document.getElementById('mlClassesCount').textContent = dsInfo.num_classes;
  document.getElementById('mlFeaturesCount').textContent = dsInfo.num_features;
  document.getElementById('mlBestModelName').textContent = metrics.selected_model;

  // Comparison Table
  const tbody = document.getElementById('mlComparisonTableBody');
  if (tbody) {
    tbody.innerHTML = models.map(m => `
      <tr style="${m.is_selected ? 'background: #f0fdf4; font-weight: 600;' : ''}">
        <td>
          ${escapeHtml(m.model_name)}
          ${m.is_selected ? '<span class="badge badge-success" style="margin-left: 0.5rem;">Selected</span>' : ''}
        </td>
        <td><strong>${(m.accuracy * 100).toFixed(2)}%</strong></td>
        <td>${(m.precision * 100).toFixed(2)}%</td>
        <td>${(m.recall * 100).toFixed(2)}%</td>
        <td><strong>${(m.f1_score * 100).toFixed(2)}%</strong></td>
      </tr>
    `).join('');
  }

  // Model comparison bar chart
  renderMLComparisonChart(models);

  // Render Confusion Matrix Heatmap Table for selected model (Random Forest)
  const selModelData = metrics.detailed_results[metrics.selected_model];
  if (selModelData && selModelData.confusion_matrix) {
    renderConfusionMatrixTable(dsInfo.classes, selModelData.confusion_matrix);
  }
}

function renderMLComparisonChart(models) {
  const ctx = document.getElementById('mlComparisonChart');
  if (!ctx) return;

  if (AppState.charts['mlComparison']) {
    AppState.charts['mlComparison'].destroy();
  }

  AppState.charts['mlComparison'] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: models.map(m => m.model_name),
      datasets: [
        {
          label: 'Accuracy (%)',
          data: models.map(m => (m.accuracy * 100).toFixed(2)),
          backgroundColor: '#16a34a',
          borderRadius: 6
        },
        {
          label: 'F1-Score (Weighted %)',
          data: models.map(m => (m.f1_score * 100).toFixed(2)),
          backgroundColor: '#0284c7',
          borderRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          min: 90,
          max: 100,
          title: { display: true, text: 'Percentage (%)' }
        }
      }
    }
  });
}

function renderConfusionMatrixTable(classes, matrix) {
  const container = document.getElementById('mlConfusionMatrixContainer');
  if (!container) return;

  let html = '<table class="data-table" style="font-size: 0.72rem; text-align: center;">';
  html += '<thead><tr><th>True \\ Pred</th>';
  classes.forEach(c => {
    html += `<th style="padding: 0.35rem; font-size: 0.65rem;" title="${c}">${c.substring(0, 4)}</th>`;
  });
  html += '</tr></thead><tbody>';

  matrix.forEach((row, rIdx) => {
    html += `<tr><td style="text-align: left; font-weight: 700; font-size: 0.68rem;">${classes[rIdx]}</td>`;
    row.forEach((val, cIdx) => {
      const isDiagonal = rIdx === cIdx;
      const bg = isDiagonal ? (val > 0 ? '#dcfce7' : '#ffffff') : (val > 0 ? '#fee2e2' : '#ffffff');
      const color = isDiagonal ? '#166534' : (val > 0 ? '#991b1b' : '#94a3b8');
      html += `<td style="background: ${bg}; color: ${color}; font-weight: ${isDiagonal ? '700' : '400'}; padding: 0.35rem;">${val}</td>`;
    });
    html += '</tr>';
  });
  html += '</tbody></table>';

  container.innerHTML = html;
}

// ==========================================================================
// Feature 11: AI Agricultural Assistant (Google Gemini)
// ==========================================================================
function initChatDrawer() {
  const drawer = document.getElementById('chatDrawer');
  const triggerBtn = document.getElementById('topbarAITrigger');
  const closeBtn = document.getElementById('chatCloseBtn');
  const sendBtn = document.getElementById('chatSendBtn');
  const input = document.getElementById('chatInput');

  if (triggerBtn && drawer) {
    triggerBtn.addEventListener('click', () => {
      drawer.classList.add('open');
      updateChatContextBadge();
    });
  }

  if (closeBtn && drawer) {
    closeBtn.addEventListener('click', () => {
      drawer.classList.remove('open');
    });
  }

  if (sendBtn && input) {
    sendBtn.addEventListener('click', () => sendChatMessage());
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        sendChatMessage();
      }
    });
  }
}

function updateChatContextBadge() {
  const badge = document.getElementById('chatContextText');
  if (!badge) return;

  const loc = AppState.location.name || 'Detecting...';
  const temp = AppState.weather && AppState.weather.current ? `${Math.round(AppState.weather.current.temperature)}°C` : 'N/A';
  const rec = AppState.lastPrediction ? AppState.lastPrediction.recommended_crop : 'None yet';

  badge.textContent = `Location: ${loc} | Weather: ${temp} | Recommendation: ${rec}`;
}

async function sendChatMessage() {
  const input = document.getElementById('chatInput');
  const messagesContainer = document.getElementById('chatMessages');
  const text = input.value.trim();
  if (!text) return;

  // Add User bubble
  appendChatBubble('user', text);
  input.value = '';

  // Add Loading Bubble
  const loadingId = 'loading-' + Date.now();
  const loadingEl = document.createElement('div');
  loadingEl.id = loadingId;
  loadingEl.className = 'chat-bubble assistant';
  loadingEl.innerHTML = '<span class="status-dot"></span> Thinking... Consulting AgriSense agronomic knowledge';
  messagesContainer.appendChild(loadingEl);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  // Build current farm context
  const farmContext = {
    location: AppState.location,
    weather: AppState.weather ? AppState.weather.current : null,
    soil: {
      nitrogen: document.getElementById('inputN') ? document.getElementById('inputN').value : null,
      phosphorus: document.getElementById('inputP') ? document.getElementById('inputP').value : null,
      potassium: document.getElementById('inputK') ? document.getElementById('inputK').value : null,
      ph: document.getElementById('inputPH') ? document.getElementById('inputPH').value : null
    },
    last_recommendation: AppState.lastPrediction
  };

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        history: AppState.chatHistory,
        context: farmContext
      })
    });
    const data = await res.json();

    // Remove loading bubble
    const l = document.getElementById(loadingId);
    if (l) l.remove();

    if (data.success) {
      appendChatBubble('assistant', data.reply);
      AppState.chatHistory.push({ role: 'user', text: text });
      AppState.chatHistory.push({ role: 'assistant', text: data.reply });
    } else {
      appendChatBubble('error', data.error || 'Failed to reach AI assistant.');
    }
  } catch (err) {
    const l = document.getElementById(loadingId);
    if (l) l.remove();
    appendChatBubble('error', 'Network error connecting to Gemini service: ' + err.message);
  }
}

function appendChatBubble(role, message) {
  const container = document.getElementById('chatMessages');
  if (!container) return;

  const bubble = document.createElement('div');
  bubble.className = `chat-bubble ${role}`;

  // Basic markdown formatting for bold and lists
  let formatted = escapeHtml(message)
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n\n/g, '<br><br>')
    .replace(/\n/g, '<br>');

  bubble.innerHTML = formatted;
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

function clearChatHistory() {
  AppState.chatHistory = [];
  const container = document.getElementById('chatMessages');
  if (container) {
    container.innerHTML = `
      <div class="chat-bubble assistant">
        Hello! I am your <strong>AgriSense Intelligent Agricultural Advisor</strong>.
        I can answer questions regarding crop selection, soil health, irrigation schedules, fertilizer management, and real-time weather impacts.
        <br><br>How can I assist your farm today?
      </div>
    `;
  }
  showToast('Chat history cleared', 'info');
}

// ==========================================================================
// Modal & Utility Helpers
// ==========================================================================
function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.add('active');
}

function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.remove('active');
}

function showToast(message, type = 'info') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  const icon = type === 'success' ? '✓' : (type === 'danger' ? '✕' : (type === 'warning' ? '⚠' : 'ℹ'));
  toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
