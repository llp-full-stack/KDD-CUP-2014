require 'csv'
file = File.open("essay_length.csv", "w")
CSV.foreach("essays.csv", headers: true, header_converters: :symbol) do |row|
	if row[:essay] != nil
		file.puts row[:projectid] + ',' + row[:essay].length.to_s
	else
		file.puts row[:projectid] + ',0'
	end
end
file.close
