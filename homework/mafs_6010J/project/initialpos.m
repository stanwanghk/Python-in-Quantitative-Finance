function alpha = initialpos(V,mu,target_ret)
    options = optimset('quadprog');
    options.Display = 'off';
    options.LargeScale = 'off';
    
    n = length(mu);
    %disp(n);
    div = 0.05;
    
    Aeq = [mu;ones(1,n)];
    beq = [target_ret;1];

    % short selling is not allowed
    LB = zeros(n,1);
    % None of the stock's weights can exceed 5%
    UB = div * ones(n,1);
    % portfolio with the constraints given
    [alpha,exitflag] = quadprog(V,[],[],[],Aeq,beq,LB,UB,[],options);
    disp(exitflag);
end