#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <cmath>
#include <climits>
#include <cfloat>
using namespace std;

int main (int argc, char *argv[]) 
{	
	// open file
	string filename=string(argv[1]), line;
//  	cout<<"Please input the filename: ";
//  	getline(cin, filename);
	ifstream infile(filename.c_str());
	string output = filename.substr(0, filename.length()-3)+"csv";
	ofstream outfile(output.c_str());

	if(infile)
	{
		// output the title for first row
        outfile<<"Task,x_target,y_target,Trial,TouchID,TouchEvent,x,y,area,TimeStamp,";
        outfile<<"distToTargetX,distToTargetY,distToTarget,distToBeginX,distToBeginY,distToBegin,disToPrevMoveX,disToPrevMoveY,disToPrevMove,";
        outfile<<"speed(pixel/s),slope(distToPrevMoveY/distToPrevMoveX),TrialTime(s),TaskTime(s),ErrorType"<<endl;

		int num1, num2, task=0, prev_trial=0, trial=0, tid;
        int target_x, target_y, dist_x, dist_y, end_x, end_y;
		double dist, area, speed, elapsed_time;
		long double time_stamp, start_time=0, begin_time;
		vector<vector<int> > x(10),y(10);
        vector<long double> time;
		string touch_event;
		stringstream ss;
        
        // find max
        int max_distToTargetX=0, max_distToTargetY=0, max_distToBeginX=0, max_distToBeginY=0, max_distToPrevMoveX=0, max_distToPrevMoveY=0;
        double max_distToTarget=0, max_distToBegin=0, max_distToPrevMove=0, max_speed=0;
        
        // find min
        int min_distToTargetX=INT_MAX, min_distToTargetY=INT_MAX, min_distToBeginX=INT_MAX, min_distToBeginY=INT_MAX, min_distToPrevMoveX=INT_MAX, min_distToPrevMoveY=INT_MAX;
        double min_distToTarget=DBL_MAX, min_distToBegin=DBL_MAX, min_distToPrevMove=DBL_MAX, min_speed=DBL_MAX;
        
        // for error type: moved, inaccurate, move out, time>0.5, multitouch
        bool error_type[]={0,0,0,0,0};
        string error_name[]={"moved", "inaccurate", "move out", "time>0.5s", "multitouch"};
        
		while(!infile.eof())
		{
			// parse...
			getline(infile, line);
			ss<<line;
			ss>>time_stamp;
			ss>>tid;
			ss>>touch_event;
            if (touch_event == "start" || touch_event == "begin" || touch_event == "move" || touch_event == "end")
            {
			    ss>>num1;
			    ss>>num2;
            }
            
			// for start
			if(touch_event=="start")
			{
                time.clear();
                target_x=num1+22;
                target_y=num2+22;
                start_time=time_stamp;
//                  task++;
                ss>>task;
				trial=0;
                outfile<<task<<","<<target_x<<","<<target_y<<",";
			}

			// for begin
			else if(touch_event=="begin")
			{                
                ss>>area;
                prev_trial = trial;
                x[tid].push_back(num1);
                y[tid].push_back(num2);
                trial++;
                if(trial>1)
                    outfile<<",,,";
                if(prev_trial!=trial)
                    outfile<<trial;
				outfile<<","<<tid<<","<<touch_event<<","<<x[tid].back()<<","<<y[tid].back()<<","<<area<<","<<setprecision(12)<<time_stamp<<",";
                
                dist_x = x[tid].back()-target_x;
				dist_y = y[tid].back()-target_y;
				dist = sqrt(dist_x*dist_x+dist_y*dist_y);
				outfile<<dist_x<<","<<dist_y<<","<<dist;
                if(abs(dist_x)>abs(max_distToTargetX))
                    max_distToTargetX=dist_x;
                if(abs(dist_y)>abs(max_distToTargetY))
                    max_distToTargetY=dist_y;
                if(abs(dist)>abs(max_distToTarget))
                    max_distToTarget=dist;

                if(abs(dist_x)<abs(min_distToTargetX))
                    min_distToTargetX=dist_x;
                if(abs(dist_y)<abs(min_distToTargetY))
                    min_distToTargetY=dist_y;
                if(abs(dist)<abs(min_distToTarget))
                    min_distToTarget=dist;
                
                begin_time=time_stamp;
                time.push_back(time_stamp);
                
                // inaccurate
                if(abs(dist_x)>22 || abs(dist_y)>22)
                {
                    error_type[1]=true;
                    outfile<<",,,,,,,,,,,"<<error_name[1];
                    outfile<<",("<<dist_x<<" "<<dist_y<<")";
                }
                outfile<<endl;
                
                // for 06-11 logdata, its start=-0.0;
                if(trial==1)
                    start_time=begin_time;
			}

			// for move or end
			else if(touch_event=="move" || (touch_event=="end" && tid>=0))
			{
				ss>>area;
                x[tid].push_back(num1);
                y[tid].push_back(num2);
				outfile<<",,,,"<<tid<<","<<touch_event<<","<<x[tid].back()<<","<<y[tid].back()<<","<<area<<","<<setprecision(12)<<time_stamp<<",";
                
                // distToTarget
				dist_x = x[tid].back()-target_x;
				dist_y = y[tid].back()-target_y;
				dist = sqrt(dist_x*dist_x+dist_y*dist_y);
				outfile<<dist_x<<","<<dist_y<<","<<dist<<",";
                if(abs(dist_x)>abs(max_distToTargetX))
                    max_distToTargetX=dist_x;
                if(abs(dist_y)>abs(max_distToTargetY))
                    max_distToTargetY=dist_y;
                if(abs(dist)>abs(max_distToTarget))
                    max_distToTarget=dist;
                
                if(abs(dist_x)<abs(min_distToTargetX))
                    min_distToTargetX=dist_x;
                if(abs(dist_y)<abs(min_distToTargetY))
                    min_distToTargetY=dist_y;
                if(abs(dist)<abs(min_distToTarget))
                    min_distToTarget=dist;
                
                // check if move out
                if(touch_event=="end")
                {
                    end_x=dist_x;
                    end_y=dist_y;
                    if(abs(end_x)>22 || abs(end_y)>22)
                        error_type[2]=true;
                }
                    
				// distToBegin
                dist_x = x[tid].back()-x[tid].front();
                dist_y = y[tid].back()-y[tid].front();
                dist = sqrt(dist_x*dist_x+dist_y*dist_y);
                outfile<<dist_x<<","<<dist_y<<","<<dist<<",";
                if(abs(dist_x)>abs(max_distToBeginX))
                    max_distToBeginX=dist_x;
                if(abs(dist_y)>abs(max_distToBeginY))
                    max_distToBeginY=dist_y;
                if(abs(dist)>abs(max_distToBegin))
                    max_distToBegin=dist;
				
                if(abs(dist_x)<abs(min_distToBeginX))
                    min_distToBeginX=dist_x;
                if(abs(dist_y)<abs(min_distToBeginY))
                    min_distToBeginY=dist_y;
                if(abs(dist)<abs(min_distToBegin))
                    min_distToBegin=dist;
				
				// distToPrevMove
				if(x[tid].size()>=2 && y[tid].size()>=2)
				{
					dist_x = x[tid].back()-x[tid][x[tid].size()-2];
					dist_y = y[tid].back()-y[tid][y[tid].size()-2];
					dist = sqrt(dist_x*dist_x+dist_y*dist_y);
					outfile<<dist_x<<","<<dist_y<<","<<dist<<",";
                    if(abs(dist_x)>abs(max_distToPrevMoveX))
                        max_distToPrevMoveX=dist_x;
                    if(abs(dist_y)>abs(max_distToPrevMoveY))
                        max_distToPrevMoveY=dist_y;
                    if(abs(dist)>abs(max_distToPrevMove))
                        max_distToPrevMove=dist;

                    if(abs(dist_x)<abs(min_distToPrevMoveX))
                        min_distToPrevMoveX=dist_x;
                    if(abs(dist_y)<abs(min_distToPrevMoveY))
                        min_distToPrevMoveY=dist_y;
                    if(abs(dist)<abs(min_distToPrevMove))
                        min_distToPrevMove=dist;
				}
				else
					outfile<<endl;

				// speed
				time.push_back(time_stamp);
				if(time.size()>=2)
				{
					elapsed_time = time.back() - time[time.size()-2];
					speed = dist/elapsed_time; //change to pixel/ms
					outfile<<speed<<",";
                    if(speed>max_speed)
                        max_speed=speed;

                    if(speed<min_speed)
                        min_speed=speed;
				}
				
				// slope
				if(dist_x==0)
					outfile<<"vertical";
				else
					outfile<<dist_y/dist_x;

				// trial time
                if(touch_event=="end")
                {
                    outfile<<","<<time.back()-begin_time<<",,";
                    if(error_type[2])
                        outfile<<error_name[2]<<",("<<end_x<<" "<<end_y<<")";
                }
                
                // print error type: moved
                if(touch_event=="move" && !error_type[0])
                {
                    error_type[0]=true;
                    outfile<<",,,"<<error_name[0];
                }
                outfile<<endl;
                
                // show max and min
                if(touch_event=="end")
                {
                    // show max
                    outfile<<",,,,,,,,,MAX,";
                    outfile<<max_distToTargetX<<","<<max_distToTargetY<<","<<max_distToTarget<<",";
                    outfile<<max_distToBeginX<<","<<max_distToBeginY<<","<<max_distToBegin<<",";
                    outfile<<max_distToPrevMoveX<<","<<max_distToPrevMoveY<<","<<max_distToPrevMove<<",";
                    outfile<<max_speed<<",,,,";
                    if(time.back()-begin_time>0.5)
                    {
                        error_type[3]=true;
                        outfile<<error_name[3]<<","<<time.back()-begin_time;
                    }
                    else
                    {
                        outfile<<","<<time.back()-begin_time;
                    }
                    outfile<<endl;

                    // show min
                    outfile<<",,,,,,,,,MIN,";
                    outfile<<min_distToTargetX<<","<<min_distToTargetY<<","<<min_distToTarget<<",";
                    outfile<<min_distToBeginX<<","<<min_distToBeginY<<","<<min_distToBegin<<",";
                    outfile<<min_distToPrevMoveX<<","<<min_distToPrevMoveY<<","<<min_distToPrevMove<<",";
                    outfile<<min_speed;
                    outfile<<endl<<endl;
                    
                    // clear to find max and min
                    max_distToTargetX=0; max_distToTargetY=0; max_distToTarget=0;
                    max_distToBeginX=0; max_distToBeginY=0; max_distToBegin=0;
                    max_distToPrevMoveX=0; max_distToPrevMoveY=0; max_distToPrevMove=0, max_speed=0;
                    
                    min_distToTargetX=INT_MAX; min_distToTargetY=INT_MAX; min_distToBeginX=INT_MAX; min_distToBeginY=INT_MAX; min_distToPrevMoveX=INT_MAX; min_distToPrevMoveY=INT_MAX;
                    min_distToTarget=DBL_MAX; min_distToBegin=DBL_MAX; min_distToPrevMove=DBL_MAX; min_speed=DBL_MAX;
                    for(unsigned i=0; i<4; i++)
                        error_type[i]=false;
                    
                    x[tid].clear();
                    y[tid].clear();
                }
			}

			// for whole task end
			else if (touch_event=="end" || touch_event=="time's")
			{
                outfile<<",,,,,,,,,,,,,,,,,,,,,,"<<time.back()-start_time<<endl<<endl;
                begin_time=time.back()+1;
            }
			
			// reset
			touch_event.clear();
            ss.str(std::string());
			ss.clear();
			line.clear();
		}

		if(outfile)
			cout<<"output to "<<output<<" successfully"<<endl;
	}
	else
		cout<<"open failed"<<endl;

	// close the files
	infile.close();
	outfile.close();

	return 0;
}



