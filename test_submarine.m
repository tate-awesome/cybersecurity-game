clear x y theta rho
%close all
global C
C=[];
v=0;
L=.07;

x=0;
y=0;
theta=0;
dt=1;
f=figure

target= [500,100];
set(f, 'WindowButtonDownFcn', @clicker);

for k=1:1000
    if isempty(C)
        target=[200,100];
    else
        target=[C(1,1) C(1,2)];
    end
    set(f, 'WindowButtonDownFcn', @clicker);
   %% Controller Computation
  
   if k>20
       attack(:,k)=0*[0;0;-theta(k)+pi/2];
   else
       attack(:,k)=[0;0;0];
   end

   sensor(:,k)=[x(k); y(k);theta(k)]+attack(:,k); 

   k
   
   
   %Compute the tip of the submarine based on position x,y, and direction angle (theta) 
   head_pos=[sensor(1,k)+20*cos(sensor(3,k)),sensor(2,k)+20*sin(sensor(3,k))]; 
    
   %computes the rudder angle (or steering angle) based on the angle
   %between x,y and the target position
    rho(k)=0.1*(atan2((target(2)-sensor(2,k)),(target(1)-sensor(1,k)))-sensor(3,k));
    if rho(k)>=pi/3
        rho(k)=pi/3;
    elseif rho(k)<=-pi/3
        rho(k)=-pi/3;
    end
    %computes the velocity of the submarine, which is proportional to the distance to the target
    %  Once the heading position reaches the target, then the velocity is 0.
     v(k)=0.5*sqrt(sum(abs((target-[head_pos(1),head_pos(2)])))); 
     if sum(abs((target-[head_pos(1),head_pos(2)])))<=0.5
         v(k)=0;
     end
    
    %% Computes the dynamic model based on the control commands (v,rho)
    %this is based on a discretized differential equation to update x,y,
    %theta (direction)

    if k>=20
        v_a(k)=v(k);
    else
        v_a(k)=v(k);
    end
    xdot=v_a(k)*cos(rho(k)+theta(k));
    ydot=v_a(k)*sin(rho(k)+theta(k));
    thetadot=0.6/(L/tan(rho(k)));

    x(k+1)=x(k)+dt*xdot;
    y(k+1)=y(k)+dt*ydot;
    theta(k+1)=theta(k)+dt*thetadot;
    hold off
    plot([x(k) x(k)+20*cos(theta(k))],[y(k) y(k)+20*sin(theta(k))],'k', LineWidth=2);
    hold on
    plot([sensor(1,k) sensor(1,k)+20*cos(sensor(3,k))],[sensor(2,k) sensor(2,k)+20*sin(sensor(3,k))],'r', LineWidth=2);
   axis([0 600 0 600])
   hold on
   plot(target(1),target(2),'xr')

   drawnow
    pause(.05)
    

end

function clicker(h,~)
global C
C=get(gca, 'currentpoint');
disp(C)
end
