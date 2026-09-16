from agent import search_agent , reader_agent , writer_chain , critic_chain

def run_research_pipeline (topic : str) -> dict :
    state= {}

    print("\n" + "="*50)
    print("Step 1 - Search Agent is Working.....")
    print("="*50)

    searchagent = search_agent()

    search_result = searchagent.invoke({
        "messages" : [{"user" , f"Find recent , reliable and detailed information about : {topic}"}]
    })

    state['search_results'] = search_result['messages'][-1].content
    print(f'\n Search Result : {state['search_results']}')


    print("\n" + "="*50)
    print("Step 2 - Reader Agent is Working.....")
    print("="*50)

    readeragent = reader_agent()
    reader_result = readeragent.invoke({
        "messages" : [("user" , 
            f"Based on the following search results about {topic}" 
            f"Pick the most relevant URLs and scrape it for deeper content . \n\n"
            f"Search results : \n{state['search_results'][:800]}"
        )]
    })
    state['scraped_results'] = reader_result['messages'][-1].content

    print(f"Scraped Result : {state['scraped_results']}")


    print("\n" + "="*50)
    print("step 3 : Writer is drafting the report")

    research_combined = (
        f'SEARCH RESULTS : {state['search_results']} \n \n'
        f'DETAILED SCRAPED CONTENT : {state['scraped_results']} \n\n'
    )

    state['report'] = writer_chain.invoke({
        "topic" : topic ,
        "research" : research_combined
    })

    print(f"\n\n FINAL REPORT : {state['report']}")

    print("\n" + "="*50)
    print("step 4 : Critic is reviewing the report")

    state['feedback'] = final_report = critic_chain.invoke({
        "report" : state['report']
    })

    print(f"Report Is ready : {final_report}")

    return state


