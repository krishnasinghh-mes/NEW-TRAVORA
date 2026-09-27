import sys
sys.stdout.reconfigure(encoding='utf-8')
import httpx

c = httpx.Client(base_url='http://127.0.0.1:8000', timeout=10.0)

tours = c.get('/api/tours').json()
assert len(tours) > 0, 'No tours found!'
tour = tours[0]
tour_id = tour['id']
tour_code = tour['code']
tour_title = tour['title']
print(f'Testing on Tour ID: {tour_id} ({tour_code} - {tour_title})')

# 1. Trigger disruption
disrupt_res = c.post(f'/api/tours/{tour_id}/disrupt').json()
assert disrupt_res['success'] == True
ce_id = disrupt_res['change_event_id']
print(f'Disruption created with Change Event ID: {ce_id}')

# 2. Verify alert is pending
alerts_after_disrupt = c.get('/api/operator/alerts').json()
pending = [a for a in alerts_after_disrupt if a['status'] == 'pending' and a['id'] == ce_id]
assert len(pending) == 1, 'Expected 1 pending alert for this event'
print(f'✓ Alert #{ce_id} is in Pending state')

# 3. Resolve change event
tour_det = c.get(f'/api/tours/{tour_id}').json()
ce = next(e for e in tour_det['change_events'] if e['id'] == ce_id)
alt_id = ce['alternatives'][0]['id']
apply_res = c.post('/api/changes/apply', json={'change_event_id': ce_id, 'alternative_id': alt_id}).json()
assert apply_res['success'] == True
print(f'✓ Applied alternative #{alt_id}: {apply_res["message"]}')

# 4. Verify Alert is now RESOLVED and removed from pending
alerts_after_resolve = c.get('/api/operator/alerts').json()
resolved_event = next(a for a in alerts_after_resolve if a['id'] == ce_id)
assert resolved_event['status'] == 'resolved'
print(f'✓ Change Event #{ce_id} is marked RESOLVED in database')

pending_after = [a for a in alerts_after_resolve if a['status'] == 'pending' and a['id'] == ce_id]
assert len(pending_after) == 0, 'Resolved event must not be in pending list!'
print('✓ Event successfully removed from pending alerts!')

tour_after = c.get(f'/api/tours/{tour_id}').json()
assert tour_after['status'] == 'active'
print(f'✓ Tour #{tour_id} status restored to ACTIVE')

print('\n==================================================================')
print('🎉 ALL ALERT RESOLUTION AND SYNC TESTS PASSED WITH 100% SUCCESS!')
print('==================================================================')
