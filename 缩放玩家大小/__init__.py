from tool_delta import event, command, player, send_command

# 体型限制，防止输入离谱数值炸服
MIN_SCALE = 0.2
MAX_SCALE = 7000000000.0

def set_player_scale(target_xuid: str, scale: float):
    """调用基岩版指令修改玩家实体缩放（模型大小）"""
    send_command(f"setactorproperty @xuid({target_xuid}) scale {scale}")

@event.player_join
def on_player_join(p: player.Player):
    """玩家进服自动重置为正常体型1.0"""
    set_player_scale(p.xuid, 1.0)

@command.register(".scale")
def cmd_scale(p: player.Player, args: list):
    """
    指令处理：
    .scale 数值        给自己改大小
    .scale ID 数值     给别人改大小
    .scale reset       重置自己
    .scale resetall    重置所有人（仅OP）
    """
    # 权限判断：非OP直接拦截
    if not p.is_admin:
        p.reply("§c你没有权限使用该指令！")
        return

    if len(args) == 0:
        p.reply("§e用法：.scale 数值 / .scale 玩家ID 数值 / .scale reset / .scale resetall")
        return

    # 重置自己
    if args[0] == "reset":
        set_player_scale(p.xuid, 1.0)
        p.reply("§a已将自身体型重置为默认")
        return

    # 重置全服
    if args[0] == "resetall":
        online_list = player.get_all_online_players()
        for one in online_list:
            set_player_scale(one.xuid, 1.0)
        p.reply(f"§a已重置全部 {len(online_list)} 名在线玩家体型")
        return

    # 给自己设置体型 .scale 1.5
    if len(args) == 1:
        try:
            scale = float(args[0])
        except ValueError:
            p.reply("§c数值必须为数字！")
            return
        scale = max(MIN_SCALE, min(scale, MAX_SCALE))
        set_player_scale(p.xuid, scale)
        p.reply(f"§a自身体型已设置为 {scale}")
        return

    # 给指定玩家设置 .scale Steve 2
    if len(args) == 2:
        target_name = args[0]
        try:
            scale = float(args[1])
        except ValueError:
            p.reply("§c缩放值格式错误！")
            return
        scale = max(MIN_SCALE, min(scale, MAX_SCALE))
        target_p = player.get_player_by_name(target_name)
        if target_p is None:
            p.reply(f"§c未找到在线玩家：{target_name}")
            return
        set_player_scale(target_p.xuid, scale)
        p.reply(f"§a已将玩家 {target_name} 体型设置为 {scale}")
        return
