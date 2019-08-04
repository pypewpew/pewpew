import pew

def start():
    pew.init()

    try:
        game()
        end_game(winner=True)
    except:
        end_game(winner=False)

def game():
    data = init_data()

    while not has_won_the_game(data):
        data = update_game(data)
        show_scene(data)
        speed = data['player']['speed']
        pew.tick(1 / speed)

def init_data():
    return {
        'player': {
            'position': [(3, 7), (4, 7)],
            'speed': 4,
        },
        'ball': {
            'position': (0, 3),
            'velocity': (1, 1),
        },
        'blocks': [ 
            [1, 2, 1, 2, 1, 2, 1, 2],
            [2, 1, 2, 1, 2, 1, 2, 1],
        ],
    }

def has_won_the_game(data):
    blocks = data['blocks']

    for row in blocks:
        for block in row:
            if block > 0:
                return False

    return True

def update_game(data):
    data = move_ball(data)
    data = move_player(data)
    return data

def move_ball(data):
    player = data['player']
    ball = data['ball']
    blocks = data['blocks']

    if has_hit_player(ball, player):
        ball = resolve_player_hit(ball, player)
    elif has_hit_block(ball, blocks):
        ball, blocks = resolve_block_hit(ball, blocks)
    elif is_game_over(ball, player):
        raise Exception('Game Over')
    else:
        xball, yball = ball['position']
        vxball, vyball = ball['velocity']
        ball['position'] = (xball + vxball, yball + vyball)

        if is_out_of_bounds(ball):
            ball = resolve_out_of_bounds(ball)

    return {'player': player, 'ball': ball, 'blocks': blocks}

def has_hit_player(ball, player):
    xball, yball = ball['position']
    return (xball, yball + 1) in player['position']

def resolve_player_hit(ball, player):
    xball, _ = ball['position']
    vxball, _ = ball['velocity']
    x1player, _ = player['position'][0]
    x2player, _ = player['position'][1]

    if vxball == 1 and (xball == x1player or xball == 7):
        xball -= 1
        vxball = -1
    elif vxball == -1 and (xball == x2player or xball == 0):
        xball += 1
        vxball = 1
    else:
        xball += vxball

    ball['position'] = (xball, 5)
    ball['velocity'] = (vxball, -1)
    return ball

def has_hit_block(ball, blocks):
    xball, yball = ball['position']
    vxball, vyball = ball['velocity']

    next_xball = xball + vxball
    next_yball = yball + vyball

    ball_copy = ball.copy()
    ball_copy['position'] = (next_xball, next_yball)

    if is_out_of_bounds(ball_copy):
        ball_copy = resolve_out_of_bounds(ball_copy)
        next_xball, next_yball = ball_copy['position']

    if has_block_alive(blocks, xball, next_yball):
        return True
    elif has_block_alive(blocks, next_xball, yball):
        return True
    elif has_block_alive(blocks, next_xball, next_yball):
        return True

    return False

def has_block_alive(blocks, x, y):
    return x >= 0 and y >= 0 and len(blocks) > y and len(blocks[y]) > x and blocks[y][x] > 0

def resolve_block_hit(ball, blocks):
    xball, yball = ball['position']
    vxball, vyball = ball['velocity']

    next_xball = xball + vxball
    next_yball = yball + vyball

    ball_copy = ball.copy()
    ball_copy['position'] = (next_xball, next_yball)

    if is_out_of_bounds(ball_copy):
        ball_copy = resolve_out_of_bounds(ball_copy)
        next_xball, next_yball = ball_copy['position']
        vxball, vyball = ball_copy['velocity']

    diagonal_hit = True

    if has_block_alive(blocks, xball, next_yball):
        diagonal_hit = False
        blocks[next_yball][xball] -= 1
        vyball = -vyball
    
    if has_block_alive(blocks, next_xball, yball):
        diagonal_hit = False
        blocks[yball][next_xball] -= 1
        vxball = -vxball

    if diagonal_hit:
        blocks[next_yball][next_xball] -= 1
        vxball = -vxball
        vyball = -vyball

    ball['velocity'] = (vxball, vyball)
    ball['position'] = (xball + vxball, yball + vyball)

    if is_out_of_bounds(ball):
        ball = resolve_out_of_bounds(ball)
    
    return (ball, blocks)

def is_game_over(ball, player):
    xball, yball = ball['position']
    x1player, _ = player['position'][0]
    x2player, _ = player['position'][1]

    return yball == 6 and xball != x1player and xball != x2player

def is_out_of_bounds(ball):
    xball, yball = ball['position']
    return xball < 0 or xball > 7 or yball < 0 or yball > 7

def resolve_out_of_bounds(ball):
    xball, yball = ball['position']
    vxball, vyball = ball['velocity']

    if xball < 0:
        vxball = 1
        xball = 1
    elif xball > 7:
        vxball = -1
        xball = 6

    if yball < 0:
        vyball = 1
        yball = 1
    elif yball > 7:
        vyball = -1
        yball = 6

    ball['position'] = (xball, yball)
    ball['velocity'] = (vxball, vyball)
    return ball

def move_player(data):
    x1player, y1player = data['player']['position'][0]
    x2player, y2player = data['player']['position'][1]

    keys = pew.keys()

    if keys & pew.K_LEFT and x1player > 0:
        x1player -= 1
        x2player -= 1
    elif keys & pew.K_RIGHT and x2player < 7:
        x1player += 1
        x2player += 1
    
    data['player']['position'] = [(x1player, y1player), (x2player, y2player)]
    return data

def show_scene(data):
    scene = new_scene()
    scene = show_blocks(scene, data['blocks'])
    scene = show_player(scene, data['player'])
    scene = show_ball(scene, data['ball'])
    pew.show(scene)

def new_scene():
    return pew.Pix()

def show_blocks(scene, blocks):
    for row, row_blocks in enumerate(blocks):
        for column, life in enumerate(row_blocks):
            scene.pixel(column, row, life)

    return scene

def show_player(scene, player):
    x1player, y1player = player['position'][0]
    x2player, y2player = player['position'][1]
    scene.pixel(x1player, y1player, 2)
    scene.pixel(x2player, y2player, 2)
    return scene

def show_ball(scene, ball):
    xball, yball = ball['position']
    scene.pixel(xball, yball, 3)
    return scene

def end_game(winner=False):
    scene = new_scene()
    message = 'You Win' if winner else 'Game Over'
    text = pew.Pix.from_text(message)
    for dx in range(-8, text.width):
        scene.blit(text, -dx, 1)
        pew.show(scene)
        pew.tick(1 / 12)

start()
