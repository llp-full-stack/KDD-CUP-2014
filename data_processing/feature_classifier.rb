file = File.open(ARGV[0], "r")
lnum = 1
feature = []
file.each_line{ |line|
	s_line = line.split
	len = s_line[1].to_i + 3
	4.upto(len) {|i|
		s = s_line[i].split(":")
		col = s[0].to_i
		val = s[1].to_i
		flen = feature.length
		(col - flen + 1).times{feature = feature + Array.new(1, Array.new)}
		feature[col] << [lnum, val]
	}
	lnum = lnum + 1
}
file.close

system("mkdir ans")
Dir.chdir("ans")

lnum = lnum - 1
flen = feature.length - 1
0.upto(flen) { |i|
	file = File.open("#{i}.csv", "w")
	ptr = 1
	feature[i].each{|x|
		(x[0]-ptr).times {file.puts 0}
		ptr = x[0] + 1
		file.puts x[1]
	}
	(lnum - ptr + 1).times {file.puts 0}
	file.close
}
