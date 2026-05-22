const API_URL = "https://smart-resume-extractor-production.up.railway.app";

let currentUser = "";
let allRepos = [];

function go(id, btn) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('on'));
    document.querySelectorAll('.tab').forEach(b => b.classList.remove('on'));
    document.getElementById(id).classList.add('on');
    if (btn) btn.classList.add('on');
}

async function fetchProfile() {
    const usernameInput = document.getElementById('usernameInput').value.trim();
    if (!usernameInput) {
        alert("Please enter a GitHub username");
        return;
    }
    
    currentUser = usernameInput;
    document.getElementById('loadingDot').style.display = 'flex';
    document.getElementById('navTabs').style.display = 'flex';
    
    // Switch to page 1
    go('p1', document.querySelector('.tab'));
    
    document.getElementById('p1Content').style.display = 'none';
    document.getElementById('p1Loading').style.display = 'block';
    
    try {
        const response = await fetch(`${API_URL}/profile-summary?username=${currentUser}`);
        if (!response.ok) throw new Error("Failed to fetch profile");
        const data = await response.json();
        
        populateProfile(data);
        populateReposList(data.repositories);
        
    } catch (error) {
        console.error(error);
        alert("Error fetching profile: " + error.message);
    } finally {
        document.getElementById('loadingDot').style.display = 'none';
        document.getElementById('p1Loading').style.display = 'none';
        document.getElementById('p1Content').style.display = 'block';
    }
}

function populateProfile(data) {
    const profile = data.profile;
    const analysis = data.profile_analysis;
    
    document.getElementById('profileName').innerText = profile.name || currentUser;
    document.getElementById('profileHandle').innerText = `@${currentUser}`;
    document.getElementById('profileLocation').innerText = `📍 ${profile.location || 'Unknown'}`;
    document.getElementById('avatarInitials').innerText = profile.name ? profile.name.substring(0,2).toUpperCase() : currentUser.substring(0,2).toUpperCase();
    
    document.getElementById('statRepos').innerText = profile.public_repos || data.repositories.length;
    document.getElementById('statFollowers').innerText = profile.followers || 0;
    
    // Calculate total stars
    const totalStars = data.repositories.reduce((acc, repo) => acc + (repo.stars || 0), 0);
    document.getElementById('statStars').innerText = totalStars;
    
    document.getElementById('profSummary').innerText = analysis.professional_summary || 'No summary available.';
    
    // Populate Skills
    const skillsWrap = document.getElementById('skillsWrap');
    skillsWrap.innerHTML = '';
    const skills = analysis.key_skills || {};
    const categories = [
        { key: 'languages', class: 'sk-py' },
        { key: 'frameworks', class: 'sk-fw' },
        { key: 'ml_tools', class: 'sk-ml' },
        { key: 'devtools', class: 'sk-tool' }
    ];
    categories.forEach(cat => {
        if (skills[cat.key]) {
            skills[cat.key].forEach(skill => {
                skillsWrap.innerHTML += `<span class="sk ${cat.class}">${skill}</span>`;
            });
        }
    });
    
    // Populate Top Jobs
    const jobsGrid = document.getElementById('jobsGrid');
    jobsGrid.innerHTML = '';
    const jobs = analysis.top_company_matches || [];
    jobs.forEach(job => {
        jobsGrid.innerHTML += `
        <div class="jc">
            <div class="jc-company">${job.company}</div>
            <div class="jc-role">${job.role}</div>
            <div class="jc-pct">${job.match_pct}%</div>
            <div class="bar"><div class="bar-fill" style="width:${job.match_pct}%"></div></div>
        </div>`;
    });
}

function populateReposList(repos) {
    allRepos = repos;
    const repoGrid = document.getElementById('repoGrid');
    repoGrid.innerHTML = '';
    
    document.getElementById('repoSubtitle').innerText = `${repos.length} public repos · select any to deep-dive`;
    
    repos.forEach(repo => {
        const desc = repo.description || 'No description provided';
        const lang = repo.language || 'Code';
        
        repoGrid.innerHTML += `
        <div class="repo-row" onclick="openDetail(this, '${repo.repo_name}', '${lang}')">
            <div class="ri">
                <div class="rn">${repo.repo_name}</div>
                <div class="rd">${desc}</div>
            </div>
            <span class="rl">${lang}</span>
            <button class="vbtn">View →</button>
        </div>`;
    });
}

async function openDetail(row, repoName, lang) {
    document.querySelectorAll('.repo-row').forEach(r => r.classList.remove('sel'));
    row.classList.add('sel');
    
    const panel = document.getElementById('detailPanel');
    const loading = document.getElementById('detailLoading');
    const content = document.getElementById('detailContent');
    
    panel.classList.add('vis');
    content.style.display = 'none';
    loading.style.display = 'block';
    panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    try {
        const response = await fetch(`${API_URL}/analyze-repo?username=${currentUser}&repo_name=${repoName}`);
        const data = await response.json();
        
        const analysis = data.analysis;
        
        document.getElementById('dTitle').innerText = repoName;
        document.getElementById('dSub').innerText = `${currentUser} · ${lang}`;
        
        const diff = analysis.difficulty_level || 'Intermediate';
        const diffEl = document.getElementById('dDiff');
        diffEl.textContent = diff.toUpperCase() === 'ADVANCED' ? '⚡ ADVANCED' : diff.toUpperCase() === 'INTERMEDIATE' ? '✦ INTERMEDIATE' : '○ BEGINNER';
        diffEl.className = 'diff ' + (diff.toUpperCase() === 'ADVANCED' ? 'adv' : 'mid');
        
        document.getElementById('dSummary').innerText = analysis.project_summary || '';
        
        document.getElementById('dFeatures').innerHTML = (analysis.main_features || [])
            .map(f => `<span class="chip">${f}</span>`).join('');
            
        document.getElementById('dBullets').innerHTML = (analysis.resume_bullets || [])
            .map(b => `<li>${b}</li>`).join('');
            
        loading.style.display = 'none';
        content.style.display = 'block';
        
    } catch(err) {
        console.error(err);
        loading.innerHTML = "Error analyzing repo.";
    }
}

async function runJobMatch() {
    const jdText = document.getElementById('jdText').value.trim();
    if (!jdText) {
        alert("Please paste a Job Description first.");
        return;
    }
    
    if (!currentUser) {
        alert("Please fetch a GitHub profile first on Page 1.");
        return;
    }
    
    document.getElementById('matchResult').style.display = 'none';
    document.getElementById('matchLoading').style.display = 'block';
    
    try {
        const response = await fetch(`${API_URL}/match-job`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: currentUser,
                job_description: jdText
            })
        });
        
        const data = await response.json();
        renderJobMatch(data);
        
    } catch (err) {
        console.error(err);
        alert("Error matching job: " + err.message);
    } finally {
        document.getElementById('matchLoading').style.display = 'none';
    }
}

function renderJobMatch(data) {
    document.getElementById('matchResult').style.display = 'block';
    
    const pct = data.match_percentage || 0;
    document.getElementById('matchPctVal').innerText = `${pct}%`;
    
    // arc length is 301.6, offset calculation
    const offset = 301.6 - (301.6 * (pct / 100));
    document.getElementById('donutArc').style.strokeDashoffset = offset;
    
    const verdictEl = document.getElementById('matchVerdict');
    verdictEl.innerText = data.final_verdict || '';
    if (pct >= 85) verdictEl.className = "verdict good";
    else if (pct < 70) verdictEl.className = "verdict bad";
    else verdictEl.className = "verdict";
    
    // Top repos
    const topRepos = document.getElementById('topReposList');
    topRepos.innerHTML = '';
    (data.top_matching_repositories || []).forEach((repo, idx) => {
        const rClass = idx === 0 ? 'r1' : idx === 1 ? 'r2' : 'r3';
        topRepos.innerHTML += `
        <div class="tr-row">
            <div class="rank ${rClass}">${idx + 1}</div>
            <div class="tr-info">
                <div class="tr-name">${repo.repo_name}</div>
                <div class="tr-reason">${repo.reason}</div>
            </div>
            <div class="tr-pct">${repo.match_percentage || ''}%</div>
        </div>
        `;
    });
    
    // Gaps and Strengths
    const gapsList = document.getElementById('gapList');
    const strengthsList = document.getElementById('strengthsList');
    gapsList.innerHTML = '';
    strengthsList.innerHTML = '';
    
    (data.missing_skills || []).forEach(gap => {
        gapsList.innerHTML += `
        <div class="gap-item">
            <div class="gi">⚡</div>
            <div class="gt"><strong>${gap}</strong></div>
        </div>`;
    });
    
    (data.strengths || []).forEach(strength => {
        strengthsList.innerHTML += `
        <div class="gap-item strength">
            <div class="gi">💪</div>
            <div class="gt"><strong>${strength}</strong></div>
        </div>`;
    });
    
    document.getElementById('gapsCard').style.display = (data.missing_skills && data.missing_skills.length > 0) ? 'block' : 'none';
}