global.window = global;
global.location = { origin: 'http://localhost:8000', href: 'http://localhost:8000' };
global.window.location = global.location;
global.document = {
  documentElement: { classList: { add() {}, remove() {} }, setAttribute() {} },
  getElementById: () => null,
  addEventListener: () => {}
};
global.localStorage = {
  getItem: () => null,
  setItem: () => {},
  removeItem: () => {}
};

async function checkOutput() {
  const { store } = await import('./static/js/store.js');
  const components = ['auth_view.js', 'landing.js'];

  for (const comp of components) {
    const mod = await import(`./static/js/components/${comp}`);
    const fnNames = Object.keys(mod).filter(k => k.startsWith('render'));
    for (const fn of fnNames) {
      const html = mod[fn]() || '';
      const regex = />([^<]*[\{\}][^<]*)</g;
      let m;
      while ((m = regex.exec(html)) !== null) {
        const text = m[1].trim();
        const start = Math.max(0, m.index - 100);
        const end = Math.min(html.length, m.index + 100);
        console.log(`FOUND IN ${comp} -> ${fn}: "${text}"`);
        console.log('CONTEXT:\n' + html.substring(start, end));
        console.log('-------------------------------------------');
      }
    }
  }
}

checkOutput();
