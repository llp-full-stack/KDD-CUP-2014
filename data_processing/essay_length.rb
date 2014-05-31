require 'csv'
file = File.open("essay_length.csv", "w")
CSV.foreach("essays.csv", headers: true, header_converters: :symbol) do |row|
	file.puts row[:projectid] + ',' + row[:essay].length.to_s
end
file.close
