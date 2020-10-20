from imprcm_query_server.db import get_sandc_summaries_by_id



def infra_sandcs_get(elr):
	print('query_server_sandcs_get')
	return 'query_server_sandcs_get' + elr

def infra_uuids_uuid_get(uuid):
	print('query_server_infra_uuids_uuid_get')
	return 'query_server_infra_uuids_uuid_get' + uuid

def infra_s_and_c_summary_get(unit_id, from_date='1900-01-01', to_date='2999-12-31'):

	results, status, error = get_sandc_summaries_by_id(unit_id)
	#print(results, status, error)

	if results:
		return results
	else:
		return error
	# return 'infra_s_and_c_summary_get'