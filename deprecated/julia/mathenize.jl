module matematicas
export compute, rest

function convert(item)

    if occursin("sin", item) == 1

        first = findfirst("(", item); first = first[1] + 1
        last = findfirst(")", item); last = last[1] - 1
        return sin(parse(Float64, item[first:last]))
        
    elseif occursin("cos", item) == 1

        first = findfirst("(", item); first = first[1] + 1
        last = findfirst(")", item); last = last[1] - 1
        return cos(parse(Float64, item[first:last])) 

    elseif occursin("tan", item) == 1

        first = findfirst("(", item); first = first[1] + 1
        last = findfirst(")", item); last = last[1] - 1
        return tan(parse(Float64, item[first:last]))

    elseif occursin("pi", item) == 1
        return pi

    elseif occursin("π", item) == 1
        return pi

    elseif occursin("sqrt", item) == 1
        first = findfirst("(", item); first = first[1] + 1
        last = findfirst(")", item); last = last[1] - 1
        if parse(Float64, item[first:last]) < 1
            return sqrt(complex(parse(Float64, item[first:last])))
        else
            return sqrt(parse(Float64, item[first:last]))
        end
        
    else
        if occursin(",", item) == 1
            item = replace(item, "," => ".")
        end
        return parse(Float64, item)
    end
end


function compute(sum::String)

    if occursin(",", sum) == 1
        sum = replace(sum, "," => ".")
    end

    try
        if occursin("pi", sum) == 1
            sum = replace(sum, "pi" => "3.141592653589793")
        elseif occursin("π", sum) == 1
            sum = replace(sum, "π" => "3.141592653589793")
        end
    catch error
        return error
    finally
        try
            sum = split(sum, " ")
            old = sum
            commence = 1
            result = 0
            total = size(sum, 1)
            operand = sum[commence+1]
            if operand == "+"
                first_op = convert(sum[1])
                second_op = convert(sum[3])
                result += first_op + second_op
                commence += 3
            elseif operand == "-"
                first_op = convert(sum[1])
                second_op = convert(sum[3])
                result += first_op - second_op
                commence += 3
            elseif operand == "*"
                first_op = convert(sum[1])
                second_op = convert(sum[3])
                result += first_op * second_op
                commence += 3
            elseif operand == "/"
                first_op = convert(sum[1])
                second_op = convert(sum[3])
                result += first_op / second_op
                commence += 3
            elseif operand == "//"
                first_op = convert(sum[1])
                second_op = convert(sum[3])
                r = first_op / second_op
                result += round(r)
                commence += 3
            elseif operand == "^"
                first_op = convert(sum[1])
                second_op = convert(sum[3])
                r = first_op ^ second_op
                result += r
                commence += 3
            elseif operand == "**"
                first_op = convert(sum[1])
                second_op = convert(sum[3])
                r = first_op ^ second_op
                result += r
                commence += 3
            end
            if total > 3
                result = rest(sum[commence:size(sum, 1)], result)
                return result
            else
                return result
            end
        catch
            if size(sum, 1) < 2
                try
                    return convert(sum[1])
                catch 
                    throw(ErrorException("SmallConvertionFailed"))
                end
            else
                return result
            end
        end
    end
end
    

function rest(sum::Array, result::Float64)
    try
        commence = 1
        if sum[1] == "+"
            result += convert(sum[2])
            commence += 2
        elseif sum[1] == "-"
            result -= convert(sum[2])
            commence += 2
        elseif sum[1] == "*"
            result *= convert(sum[2])
            commence += 2
        elseif sum[1] == "/"
            result /= convert(sum[2])
            commence += 2
        elseif sum[1] == "//"
            result /= convert(sum[2])
            result = round(result)
            commence += 3
        elseif sum[1] == "^"
            result ^= convert(sum[2])
            commence += 3
        elseif sum[1] == "**"
            result ^= convert(sum[2])
            commence += 3
        end
        if commence < size(sum, 1) + 1
            result = rest(sum[commence:size(sum, 1)], result)
        end
    catch error
        throw(ErrorException("ErrorAfterSuccess"))
    finally
        return result
    end
end
end

