conf = File.open("conf", "r")
source = File.open("test.csv", "r")
exciting = File.open("exciting", "w")
output = File.open("test1.csv", "w")

f = Array.new
while (not conf.eof)
	line = conf.readline.strip
	f << line if line != ""
end

while (not source.eof)
	hash = Hash.new
	data = source.readline.split(' ')
	exciting << data[0] << "\n"
	data[4...data.size].each {|item| hash.store(*item.split(':'))}
	for i in 1..f.size
		expr = f[i-1].split(' ').map { |item| item[0] != '$' ? item : hash[item.delete('$')].to_i}.join
		val = eval(expr)
		output << "#{source.lineno} #{i} #{val}\n" unless val.zero?
	end
end

output.close
source.close
exciting.close
conf.close
