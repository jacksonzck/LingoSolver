if __name__ == "__main__":
    # Assumptions 
    # A min = 1 max = 36
    # B min = 1 max = 36
    fibs = [0, 1]
    for i in range(136):
        fibs.append(fibs[-1] + fibs[-2])
    for i in fibs[2:37]:
        print(f"movi R0 {i}\njmp Mx4")
    for i in fibs[2:37]:
        print(f"subi Mx8 {i} R0\nexit")
    pass