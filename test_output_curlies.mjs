// Mock minimal browser globals for testing
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
  const components = [
    'navbar.js',
    'auth_view.js',
    'landing.js',
    'traveler_dashboard.js',
    'trip_planner.js',
    'itinerary_view.js',
    'operator_dashboard.js',
    'business_operator.js',
    'admin_dashboard.js',
    'login_popup.js'
  ];

  for (const comp of components) {
    const mod = await import(`./static/js/components/${comp}`);
    const fnNames = Object.keys(mod).filter(k => k.startsWith('render'));
    for (const fn of fnNames) {
      const html = mod[fn]() || '';
      // Look for `{` in HTML content (excluding script or style or SVG if any)
      const lines = html.split('\n');
      lines.forEach((line, idx) => {
        if (line.includes('{{') || line.includes('{ {') || line.includes('undefined') || line.includes('NaN')) {
          console.log(`[SUSPECT] ${comp} -> ${fn} Line ${idx+1}: ${line.trim()}`);
        }
      });
    }
  }
}

checkOutput();
