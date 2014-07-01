conf = File.open("conf", "r")
source = File.open("test.csv", "r")
exciting = File.open("exciting", "w")
output = File.open("output", "w")
output1 = File.open("normal", "w")

f = Array.new
while (not conf.eof)
	line = conf.readline.strip
	f << line if line != ""
end

sum = []
max = []
min = []
map = []
ndata = 0

1.upto(f.size).each do |i|
	sum[i] = max[i] = 0.0
	min[i] = 9.9E99
end

while (not source.eof)
	hash = Hash.new
	data = source.readline.split(' ')
	exciting << data[0] << "\n"
	data[4...data.size].each {|item| hash.store(*item.split(':'))}
	map[source.lineno] = []
	for i in 1..f.size
		expr = f[i-1].gsub(/\$\d*/) { |item| hash[item.delete('$')].to_i}
		val = eval(expr)
		output << "#{source.lineno} #{i} #{val}\n" unless val.zero?
		sum[i] += val
		max[i] = [max[i], val].max
		min[i] = [min[i], val].min
		map[source.lineno][i] = val
	end
	ndata = source.lineno
end

1.upto(f.size).each do |i|
	sum[i] /= ndata
	max[i] -= sum[i]
	min[i] -= sum[i]
end
1.upto(ndata).each do |i|
	1.upto(f.size).each do |j|
		map[i][j] -= sum[j]
		nor = [max[j].abs, min[j].abs].max
		map[i][j] /= nor unless nor.zero?
		output1 << "#{i} #{j} #{map[i][j]}" << "\n"
	end
end
output.close
output1.close
source.close
exciting.close
conf.close
