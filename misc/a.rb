require 'csv'
writer = CSV.open('mycsvfile.csv','w')
begin
	print "Enter Contact Name: "
	name = STDIN.gets.chomp
	print "Enter Contact No: "
	num = STDIN.gets.chomp
	s = name+" "+num
	row1 = s.split
	writer << row1
	print "Do you want to add more ? (y/n): "
	ans = STDIN.gets.chomp
end while ans != "n"
writer.close
file = File.new('mycsvfile.csv')
lines = file.readlines
parsed = CSV.parse(lines.to_s)
p parsed
puts ""
puts "Details of Contacts stored are as follows..."
puts ""
puts "-------------------------------"
puts "Contact Name | Contact No"
puts "-------------------------------"
puts ""
CSV.open('mycsvfile.csv','r') do |row|
	puts row[0] + " | " + row[1]	
	puts ""
end