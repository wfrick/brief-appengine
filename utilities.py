from model import Article

def agolo_to_object(agolo, search_id, URL):

	try:
		summary = eval(agolo)
		sentences = summary['summary'][0]['sentences']
		title = summary['title']
		source = summary['summary'][0]['metadata']['source']
		final_summary = ''
		for sentence in sentences:
			final_summary = final_summary + sentence + '... '
		final_summary = final_summary.decode('ascii','ignore')

		result = Article(search_id=search_id,summary=final_summary,
	    	URL=URL,title=title,source=source,votes=0)

	except:
		result = "Error"
	
	return result