from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

def generate_script(subject, video_length, creativity, language, api_key):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "請為‘{subject}’為主題的影片像一個吸引人的標題, 主題語言：{language}。")
        ]
    )

    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位短影片頻道的博主。根據以下標題和相關資訊，以標題所用語言寫一個短影片腳本。

                影片標題：{title}  
                影片時長：{duration}分鐘  
                影片語言：{language}
                
                生成的腳本長度應盡量符合影片時長要求，確保內容豐富但不過長。
                
                腳本結構要求：  
                1. **開頭**：抓住觀眾的注意力，快速引入話題，製造興趣，激發觀看欲望。  
                2. **中間**：提供乾貨內容，分享有價值的資訊，確保內容簡潔、實用並保持輕鬆有趣的語氣，適合年輕觀眾。  
                3. **結尾**：給觀眾一個驚喜，或是提出引人深思的問題，或是邀請觀眾互動、評論，增加參與感。  
                
                腳本表達方式需要保持幽默、輕鬆、富有創意，確保能夠吸引年輕觀眾。**請注意：腳本的語言應與標題語言一致。如果標題是英文，則生成英文腳本；如果標題是中文，則生成中文腳本；以此類推。**  
                
                如果有相關資訊來自維基百科，請結合以下搜尋結果作為參考：  
                ```{wikipedia_search}```  
                
                但請忽略與主題無關的內容，確保腳本聚焦於影片的核心內容。

                """)
        ]
    )

    model = ChatOpenAI(openai_api_key=api_key, temperature=creativity, openai_api_base="https://api.aigc369.com/v1")

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject": subject, "language": language}).content

    search = WikipediaAPIWrapper()
    search_result = search.run(subject)

    script = script_chain.invoke({"title": title, "duration": video_length, "language": language, "wikipedia_search": search_result}).content

    return search_result, title, script

#result = generate_script("x japan樂團", 1, 0.7, my_api_key)
#print("wiki: ", result[0])
#print("\ntitle: ", result[1])
#print("\nscript: ", result[2])

