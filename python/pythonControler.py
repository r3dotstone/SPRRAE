#Zoe's attempt to turn Matlab controler into python

#     if(mod(i,100)==0)
#             e_omega =  target - theta;
#             ei_omega = ei_omega + e_omega*dt;
#             omega = 0.1 + kp_omega*e_omega + ki_omega*ei_omega;
#        end


kp_omega = 0.01
ki_omega = 0.001
#1/3 of a second delay for time delay of controler

target = 360*(0.1*dt*i)/(2*pi)
theta = 360*atan2(ym(i),xm(i))/(2*pi)

output_angle = 2
desired_angle = 1

while True :
    e_omega = target - theta
    ei_omega = ei_omega + e_omega*dt
    omega = 0.1 + kp_omega*e_omega + ki_omega*ei_omega


