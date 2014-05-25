f = open('outcomes.csv','r')
titleline = f.readline
title = titleline.chomp.split(',')
g = Array.new
range = 1.upto(title.size-4)
range.each do |i|
	filename = "#{title[i]}.csv"
    g[i] = open(filename, 'w')
	g[i] << titleline
end
while (not f.eof)
  line = f.readline
  arr = line.split(',')
  range.each do |i|
      g[i] << line if arr[i] == 't'
  end
end
range.each do |i|
    g[i].close
end