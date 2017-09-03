function alpha = portfolio(V,mu,alpha_0,target_ret)
    % turn off display and large-scale method in
    % quadratic programming
    options = optimset('quadprog');
    options.Display = 'off';
    options.LargeScale = 'off';
    
    n = length(mu);
    div = 0.05;
    turnover = 0.4;
    H = [[V,-V];[-V,V]];
    f = alpha_0*[V,-V];
    Aeq = [[mu, -mu];[ones(1,n),-ones(1,n)]];

    beq = [target_ret-mu*alpha_0';0];

    % short selling is not allowed
    LB = zeros(2*n,1);
    % None of the stock's weights can exceed 5%
    % Turnover of the portfolio should not exceed 40%
    A = [ones(1,2*n);[eye(n),-eye(n)];[-eye(n),eye(n)]];
    b = [turnover;div*ones(n,1)-alpha_0';alpha_0'];
    % portfolio with the constraints given
    [x,exitflag] = quadprog(H,f',A,b,Aeq,beq,LB,[],[],options);
    alpha = x(1:n)-x(n+1:2*n)+alpha_0';
    disp(exitflag);
end
