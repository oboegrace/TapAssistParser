
module Enumerable

    def sum
      self.inject(0){|accum, i| accum + i }
    end

    def mean
      self.sum/self.length.to_f
    end

    def sample_variance
      m = self.mean
      sum = self.inject(0){|accum, i| accum +(i-m)**2 }
      sum/(self.length - 1).to_f
    end

    def standard_deviation
      return Math.sqrt(self.sample_variance)
    end

end 

class Stroke
	def initialize(touch_id)
		@touch_id = touch_id
		@points = []
		@multi_touch = false
	end
	def add_point(time, x, y, pressure)
		@points << {
			:time => time,
			:x => x,
			:y => y,
			:pressure => pressure
		}
	end
	def x
		@points.collect{|p|p[:x]}
	end
	def y
		@points.collect{|p|p[:y]}
	end
	def time
		@points.collect{|p|p[:time]}
	end
	def speed
		v = []
		x_pos = x
		y_pos = y
		prev_x = x_pos[0]
		prev_y = y_pos[0]
		prev_time = time[0]
		for i in 1..x_pos.length-1
			x_offset = x_pos[i]-prev_x
			y_offset = y_pos[i]-prev_y
			if (time[i] != prev_time)
				v << Math.sqrt(x_offset*x_offset+y_offset*y_offset)/(time[i]-prev_time)
			end
			prev_time = time[i]
			prev_x = x_pos[i]
			prev_y = y_pos[i]
		end
		v
	end
	def begin_x
		@points.first[:x]
	end
	def begin_y
		@points.first[:y]
	end
	def begin_time
		@points.first[:time]
	end
	def end_x
		@points.last[:x]
	end
	def end_y
		@points.last[:y]
	end
	def end_time
		@points.last[:time]
	end
	def time_duration
		@points.last[:time]-@points.first[:time]
	end 
	def movement?
		x.uniq.length != 1 || y.uniq.length != 1 
	end
	def offset_x
		end_x - begin_x
	end
	def offset_y
		end_y - begin_y
	end
	def touch_id
		@touch_id
	end
	def multi_touch
		@multi_touch
	end
	def to_s
		"#{begin_time}: stroke from (#{begin_x}, #{begin_y}) to (#{end_x}, #{end_y}), #{end_time-begin_time}s"
	end
	def to_csv_row
		[
			0,
			0,
			0,
            begin_time,
			touch_id,
			begin_x,
			begin_y,
			if movement? then 1 else 0 end,
			x.max,
			y.max,
			x.min,
			y.min,
			x.mean,
			y.mean,
			x.standard_deviation,
			y.standard_deviation,
			offset_x,
			offset_y,
			speed.max,
			speed.min,
            speed.mean,
			speed.standard_deviation,
			time_duration,
			if multi_touch then 1 else 0 end,
		].join(',')
	end
	def update_multi_touch(multi_touch)
		@multi_touch = @multi_touch || multi_touch
	end
end
header = [
	'Task',
	'Attemp',
	'target',
    'begin_time',
	'TouchID',
	'touchBegin_x',
	'touchBegin_y',
	'HasMovement',
	'max_x',
	'max_y',
	'min_x',
	'min_y',
	'ave_x',
	'ave_y',
	'SD_x',
	'SD_y',
	'x_end-begin',
	'y_end-begin',
	'Max_speed',
	'Min_speed',
	'Ave_speed',
	'SD_speed',
	'time_duration',
	'multi-touch'
]
puts header.join(',')
output_strokes = []
working_strokes = {}
#  Dir.glob('UIInternalEvent *_Scroll_Hard.txt').each{|filename|
Dir.glob('dd.txt').each{|filename|
	# puts filename
	line_count = 0
	File.read(filename).split("\n").each{|s|
		line_count = line_count + 1
		# puts "line: #{line_count}"
		s = s.split(' ')
		timestamp = s[0].to_f
		mode = s[1].to_i
		touch_id = s[2].to_i
		event_desc = s[3]
		x = s[4].to_i
		y = s[5].to_i
		pressure = s[6].to_f
		working_strokes.keys.each{|s|
			working_strokes[s].update_multi_touch(working_strokes.size>1)
		}
		case event_desc
		when "begin"
			working_strokes.each{|s|
				}[touch_id] = Stroke.new(touch_id)
			working_strokes[touch_id].add_point(timestamp, x, y, pressure)
		when "move", "stationary"
			if working_strokes[touch_id].nil?
				working_strokes[touch_id] = Stroke.new(touch_id)
			end
			working_strokes[touch_id].add_point(timestamp, x, y, pressure)
        when "end"
			if !working_strokes[touch_id].nil?
				working_strokes[touch_id].add_point(timestamp, x, y, pressure)
				# output_strokes << working_strokes[touch_id]
				puts working_strokes[touch_id].to_csv_row
				working_strokes.delete(touch_id)
			end
		end
	}
}
# puts output_strokes
