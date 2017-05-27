function alpha = initialpos(V,mu,target_ret)
  options = optimset('quadprog');
    options.Display = 'off';
    options.LargeScale = 'off';
    
    n = length(mu);
    div = 0.5;
    H = V;
    
    Aeq = [mu;ones(1,n)];
    beq = [target_ret;1];

    % short selling is not allowed
    LB = zeros(n,1);
    % None of the stock's weights can exceed 5%
    UB = div * ones(n,1);
    % portfolio with the constraints given
    x = quadprog(H,[],[],[],Aeq,beq,LB,UB,[],options);
    alpha = x(1:n);
end