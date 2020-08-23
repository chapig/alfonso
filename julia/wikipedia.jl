module wikisearch
export set_lang, search

using Cascadia
using Gumbo
using HTTP

global LANG = "es"

function set_lang(language)
    
    global LANG = language

end 

function search(srch::String, ns::Int64, in_cache::Bool)
    
    name_articles = []
    saved_articles = []

    if ns == 1
        ns = 2
    end

    try

        if uppercase(srch) in name_articles

            return saved_article[indexin(uppercase(srch), name_articles)]
        else  
            sntc = []
            url = "https://$(LANG).wikipedia.org/w/index.php?sort=relevance&search=$(replace(srch, r"[\s]" => "%20"))"
            res = HTTP.get(url)

            body = String(res.body)
            html = parsehtml(body)
            title = eachmatch(sel".firstHeading", html.root)
            sentences = eachmatch(sel"p", html.root)

            for elem in sentences
                global temp = replace(text(elem), r"\[ \d \]" => s"")
                push!(sntc, replace(text(elem), r"\[ \d \]" => s""))
            end

            if in_cache
                push!(name_articles, uppercase(srch))
                push!(saved_articles, temp)
                global temp = nothing
            end
        end

        result = join(sntc[1:ns])
        result = replace(result, r"[\s][\s]" => " ")
        result = replace(result, r"[\s][\s]" => " ")
        return result

    catch error

        return error
        #throw(ErrorException("NotFoundOnWikipedia"))
        
    end
end
end