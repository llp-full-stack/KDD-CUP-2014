require 'csv'

prediction = File.open("prediction.csv", "r")
id = File.open("test_report.txt", "r")
csv = CSV.open("submission.csv", "w")
csv << ['projectid', 'is_exciting']
prediction.each_line do |line|
	id_str = id.gets
	csv << [id_str.chomp, line.chomp]
end

csv.close
id.close
prediction.close