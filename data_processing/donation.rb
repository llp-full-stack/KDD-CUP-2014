require 'csv'
require 'time'
require 'set'

class TimeReader
	def self.readStamp(string)
		time = Time.strptime(string[0, 19], "%F %R:%S")
		time - Time.strptime("2011-01-01 00:00:00", "%F %R:%S")
	end
end

class BoolReader
	def self.reader(c)
		if c == 't' then 1
		else 0
		end
	end
end

class DollarAmount
	def self.classify(string)
		if string == "10_to_100" then 1
		elsif string == "under_10" then 0
		else 2
		end
	end
end

class PaymentMethod
	def self.classify(string)
		case
		when string == "no_cash_received"
			return 0
		when string == "creditcard"
			return 1
		when string == "paypal"
			return 2
		when string == "amazon"
			return 3
		when string == "promo_code_match"
			return 4
		when string == "check"
			return 5
		when string == "double_your_impact_match"
			return 6
		when string == "almost_home_match"
			return 7
		end
	end
end

class Donation
	attr_reader :donation_id, :project_id, :is_teacher_acct, :time_stamp, :donation_to_project,\
		:donation_optional_support, :donation_total, :dollar_amount, :donation_included_optional_support,\
		:payment_method, :payment_included_acct_credit, :payment_included_campaign_gift_card,\
		:payment_included_web_purchased_gift_card, :payment_was_promo_matched, :via_giving_page,\
		:for_honoree

	@@donations = Set.new

	def initialize(row)
		@donation_id = row[:donationid]
		@project_id = row[:projectid]
		@donor_id = row[:donor_acctid]
		@city = row[:donor_city]
		@state = row[:donor_state]
		@zip = row[:donor_zip]
		@is_teacher_acct = BoolReader.reader(row[:is_teacher_acct])
		@time_stamp = TimeReader.readStamp(row[:donation_timestamp])
		@donation_to_project = row[:donation_to_project]
		@donation_optional_support = row[:donation_optional_support]
		@donation_total = row[:donation_total]
		@dollar_amount = DollarAmount.classify(row[:dollar_amount])
		@donation_included_optional_support = BoolReader.reader(row[:donation_included_optional_support])
		@payment_method = PaymentMethod.classify(row[:payment_method])
		@payment_included_acct_credit = BoolReader.reader(row[:payment_included_acct_credit])
		@payment_included_campaign_gift_card= BoolReader.reader(row[:payment_included_campaign_gift_card])
		@payment_included_web_purchased_gift_card= BoolReader.reader(row[:payment_included_web_purchased_gift_card])
		@payment_was_promo_matched= BoolReader.reader(row[:payment_was_promo_matched])
		@via_giving_page= BoolReader.reader(row[:via_giving_page])
		@for_honoree= BoolReader.reader(row[:for_honoree])
		@donation_message = row[:donation_message]
		Project.add_donation(self)
	end

	def self.scan(filename)
		CSV.foreach(filename, headers: true, header_converters: :symbol) do |row|
			donation = Donation.new(row)
			@@donations.add(donation)
		end
	end

end

class Project
	@@projects = Hash.new(0)
	attr_accessor :project_id, :donations, :donor_tot, :donor_is_teacher_acct, :timestamp_sum,\
		:donation_to_project, :donation_optional_support, :donation_total, :dollar_amount_level,\
		:donation_included_optional_support, :payment_method, :payment_included_acct_credit,\
		:payment_included_campaign_gift_card, :payment_included_web_purchased_gift_card,\
		:payment_was_promo_matched, :via_giving_page, :for_honoree 

	def initialize(id)
		@project_id = id
		@donations = Set.new
		@donor_tot = 0
		@donor_is_teacher_acct = 0
		@timestamp_sum = 0
		@donation_to_project = @donation_optional_support = @donation_total = 0
		@dollar_amount_level = [0, 0, 0]
		@donation_included_optional_support = 0
		@payment_method = Array.new(8, 0)
		@payment_included_acct_credit = @payment_included_campaign_gift_card = \
			@payment_included_web_purchased_gift_card = @payment_was_promo_matched =\
			@via_giving_page = @for_honoree = 0
		@@projects[project_id] = self
	end

	def self.projects
		@@projects
	end

	def self.add_donation(donation)
		project_id = donation.project_id
		if @@projects[project_id] == 0 then
			project = Project.new(project_id)
		else
			project = @@projects[project_id]
		end
		project.donations.add(donation)
		project.donor_tot += 1
		project.donor_is_teacher_acct += donation.is_teacher_acct
		project.timestamp_sum += donation.time_stamp
		project.donation_to_project += donation.donation_to_project.to_f
		project.donation_optional_support += donation.donation_optional_support.to_f
		project.donation_total += donation.donation_total.to_f
		project.dollar_amount_level[donation.dollar_amount] += 1
		project.donation_included_optional_support += donation.donation_included_optional_support 
		project.payment_method[donation.payment_method] += 1
		project.payment_included_acct_credit += donation.payment_included_acct_credit
		project.payment_included_campaign_gift_card += donation.payment_included_campaign_gift_card
		project.payment_included_web_purchased_gift_card += donation.payment_included_web_purchased_gift_card 
		project.payment_was_promo_matched += donation.payment_was_promo_matched
		project.via_giving_page += donation.via_giving_page
		project.for_honoree += donation.for_honoree 
	end

	def write_to_csv(csv)
		csv << [@project_id, @donor_tot, @donor_is_teacher_acct, @timestamp_sum/@donor_tot, @donation_to_project,\
		@donation_optional_support, @donation_total, @dollar_amount_level[0], @dollar_amount_level[1], @dollar_amount_level[2],\
		@donation_included_optional_support, @payment_method[0], @payment_method[1], @payment_method[2], @payment_method[3],\
		@payment_method[4], @payment_method[5], @payment_method[6], @payment_method[7], @payment_included_acct_credit,\
		@payment_included_campaign_gift_card, @payment_included_web_purchased_gift_card, @payment_was_promo_matched,\
		@via_giving_page, @for_honoree]
	end

end

i = 0

CSV.foreach("./donations.csv", headers: true, header_converters: :symbol) do |row|
	puts "donations: " + row[:donationid] + "; projects: " + row[:projectid] if i % 1000 == 0
	i += 1
	Project.add_donation(Donation.new(row))
end

CSV.open("./donation_data.csv", "wb") do |csv|
	csv << %w{project_id donor_tot donor_is_teacher_acct time_stamp donation_to_project donation_optional_support\
		donation_total dollar_amount_level_0 dollar_amount_level_1 dollar_amount_level_2 donation_included_optional_support\
		payment_method_0 payment_method_1 payment_method_2 payment_method_3 payment_method_4 payment_method_5\
		payment_method_6 payment_method_7 payment_included_acct_credit payment_included_campaign_gift_card\
		payment_included_web_purchased_gift_card payment_was_promo_matched via_giving_page for_honoree}
	Project.projects.each do |k, v|
		puts "projects:  " + v.project_id if i % 1000 == 0
		i += 1
		v.write_to_csv(csv)
	end
end
	

