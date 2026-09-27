// Mock minimal browser globals for testing component rendering in Node
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

async function testAll() {
  try {
    const { store } = await import('./static/js/store.js');
    console.log('Store imported successfully. Initial state:', store.getState().currentView);

    const components = [
      'navbar.js',
      'auth_view.js',
      'landing.js',
      'traveler_dashboard.js',
      'trip_planner.js',
      'itinerary_view.js',
      'disruption_hub.js',
      'operator_dashboard.js',
      'operator_tour_detail.js',
      'alert_center.js',
      'vendor_management.js',
      'analytics_view.js',
      'trip_tracker.js',
      'booking_modal.js',
      'review_modal.js',
      'ai_assistant.js',
      'profile_modal.js',
      'add_experience_modal.js',
      'operator_registration_modal.js',
      'operator_detail_modal.js',
      'about.js',
      'footer.js',
      'business_operator.js',
      'admin_dashboard.js',
      'feedback_modal.js',
      'login_popup.js',
      'weather_digital_twin.js'
    ];


    for (const comp of components) {
      try {
        const mod = await import(`./static/js/components/${comp}`);
        const fnNames = Object.keys(mod).filter(k => k.startsWith('render'));
        for (const fn of fnNames) {
          try {
            const html = mod[fn]();
            console.log(`[PASS] ${comp} -> ${fn}() produced ${typeof html} (${(html||'').length} chars)`);
          } catch (renderErr) {
            console.error(`[FAIL RENDER] ${comp} -> ${fn}():`, renderErr.message);
          }
        }
      } catch (importErr) {
        console.error(`[FAIL IMPORT] ${comp}:`, importErr.message);
      }
    }
  } catch (e) {
    console.error('Test error:', e);
  }
}

testAll();
