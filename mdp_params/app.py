import streamlit as st
import re

gamma = 1
def is_number(s):
    return re.match('^-?\d*\.?\d*$', s) != None

def calculate_g(S, A, trajectories):
	st.write('G:')
	cols = st.columns(len(trajectories))
	
	for i,t in enumerate(trajectories):
		with cols[i]:
			st.write(f'Trajectories {i}: ')
			t = t.split()
			for j in range(len(t)):
				if t[j].startswith('S'):
					g = sum([float(t[k]) for k in range(j+1, len(t)) if is_number(t[k])])
					st.write(f'G({t[j]}): {g}')

def count_state_action(s, a, trajectories):
    count = 0
    for t in trajectories:
        t = t.split()
        for i in range(len(t)):
            if t[i] == s and t[i+1] == a:count+=1
    return count

def count_state_action_state(s, a, s_, trajectories):
    count = 0
    for t in trajectories:
        t = t.split()
        for i in range(len(t)):
            if t[i] == s and t[i+1] == a and (t[i+2] == s_ or t[i+3] == s_):count+=1
    return count

def calculate_reward(S, A, trajectories):
    R = {}
    for s in S:
        for a in A:
            key = s,a
            if key not in R:
                count_sa = count_state_action(s, a, trajectories)
                if count_sa > 0:
                    r = calculate_total_reward(s, a, trajectories)
                    R[key] = r/count_sa
    return R

def calculate_total_reward(s, a, trajectories):
    r = 0
    for t in trajectories:
        t = t.split()
        for i in range(len(t)):
            if t[i] == s and t[i+1] == a and is_number(t[i+2]):r += float(t[i+2])
    return r

def calculate_state_value(S, A, trajectories):
    V = {}
    for s in S:
        V[s] = []
    for t in trajectories:
        t = t.split()
        for i in range(len(t)):
            if t[i].startswith('S'):
                g = sum([float(t[j]) for j in range(i+1, len(t)) if is_number(t[j])])
                V[t[i]].append(g)
    for s,v in V.items():
        V[s] = sum(v)/len(v)
    
    return V

def calculate_action_value(S, A, trajectories):
    Q = {}
    for t in trajectories:
        t = t.split()
        for i in range(len(t)):
            if t[i][0] == 'S' and t[i+1][0] == 'A':
                key = t[i],t[i+1]
                if key not in Q:
                    Q[key] = []
                g = sum([float(t[j]) for j in range(i+2, len(t)) if is_number(t[j])])
                Q[key].append(g)
    for k,v in Q.items():
        Q[k] = sum(v)/len(v)
    return Q

def calculate_prob(S, A, trajectories):
    P = {}
    for s in S:
        for a in A:
            count_sa = count_state_action(s, a, trajectories)
            if count_sa != 0:
                for s_ in S:
                    count_sas = count_state_action_state(s, a, s_, trajectories)
                    P[(s,a,s_)] = count_sas/count_sa
    return P

text = st.text_area('Input', value='S3 A1 S1 A2 S2 A1 0.1 S3 A2 1 T\nS1 A2 -0.1 S1 A1 S3 A1 S2 A2 -0.1 S3 A2 1 T')
if st.button('OK'):
    trajectories = text.splitlines()
    # G = [sum([float(s) for s in t.split() if is_number(s)]) for t in trajectories]
    # st.write('G:', *G)
    
    S,A = [],[]
    for t in trajectories:
        S.extend([s for s in t.split() if s.startswith('S')])
        A.extend([s for s in t.split() if s.startswith('A')])
    S = set(S)
    A = set(A)
    
    calculate_g(S, A, trajectories)
    
    V = calculate_state_value(S, A, trajectories)
    st.write('V:', V)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        Q = calculate_action_value(S, A, trajectories)
        for k,v in Q.items():
            st.write('Q',k,v)
    
    with col2:
        P = calculate_prob(S,A,trajectories)
        for k,v in P.items():
            st.write('P',k,v)

    with col3:
        R = calculate_reward(S, A, trajectories)
        for k,v in R.items():
            st.write('R',k,v)

# with open('input.txt') as f:
    # trajectories = f.readlines()

# G = [sum([float(s) for s in t.split() if is_number(s)]) for t in trajectories]
# print(f'G: {G}')

# S = []
# A = []
# for t in trajectories:
    # S.extend([s for s in t.split() if s.startswith('S')])
    # A.extend([s for s in t.split() if s.startswith('A')])
# S = set(S)
# A = set(A)
# print(S, A)

# V = calculate_state_value(S, A, trajectories)
# print(f'V: {V}')

# Q = calculate_action_value(S, A, trajectories)
# print(f'Q: {Q}')

# P = calculate_prob(S,A,trajectories)
# print(f'P: {P}')

# R = calculate_reward(S, A, trajectories)
# print(f'R: {R}')