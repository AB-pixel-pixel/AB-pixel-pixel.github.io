(() => {
  const storage = { get() { try { return localStorage.getItem('sl-language'); } catch { return null; } }, set(value) { try { localStorage.setItem('sl-language', value); } catch {} } };
  let language = storage.get() === 'zh' ? 'zh' : 'en';
  let filter = 'all';
  function announceCount() {
    const status = document.querySelector('.filter-status');
    if (status) {
      const count = document.querySelectorAll('.paper:not([hidden])').length;
      status.textContent = language === 'zh' ? `显示 ${count} 篇论文` : `Showing ${count} publications`;
    }
  }
  function setLanguage(next) {
    language = next;
    document.documentElement.lang = next === 'zh' ? 'zh-CN' : 'en';
    document.querySelectorAll('[data-en][data-zh]').forEach(node => { node.textContent = node.dataset[next]; });
    document.querySelectorAll('[data-language]').forEach(button => {
      button.textContent = next === 'en' ? '中文 ↔' : 'EN ↔';
      button.setAttribute('aria-label', next === 'en' ? 'Switch to Chinese' : '切换为英文');
    });
    storage.set(next);
    announceCount();
  }
  document.querySelectorAll('[data-language]').forEach(button => button.addEventListener('click', () => setLanguage(language === 'en' ? 'zh' : 'en')));
  document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
    filter = button.dataset.filter;
    document.querySelectorAll('[data-filter]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    document.querySelectorAll('.paper').forEach(item => { item.hidden = filter === 'first' && item.dataset.first !== 'true'; });
    announceCount();
  }));
  const dialog = document.querySelector('#video-dialog');
  if (dialog) {
    const video = dialog.querySelector('video');
    let opener;
    document.querySelectorAll('[data-video]').forEach(button => button.addEventListener('click', () => {
      opener = button;
      const paper = button.closest('.paper');
      document.querySelector('#video-title').textContent = paper.querySelector('h3').textContent;
      video.src = button.dataset.video;
      dialog.showModal();
      document.body.classList.add('dialog-open');
    }));
    const close = () => dialog.close();
    dialog.querySelector('.dialog-close').addEventListener('click', close);
    dialog.addEventListener('click', event => { if (event.target === dialog) { const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) close(); } });
    dialog.addEventListener('close', () => { video.pause(); video.removeAttribute('src'); video.load(); document.body.classList.remove('dialog-open'); opener?.focus(); });
  }
  setLanguage(language);
})();
