import pstats
import array
p = pstats.Stats('profiling')
p.sort_stats('time').print_stats(20)
#p.print_callers('next_int')
