# 背景：在使用 Python 进行《我是动物饲养员》这个游戏的开发过程中，有一个代码片段要求定义动物园、动物、猫、狗四个类。

# 这个类可以使用如下形式为动物园增加一只猫：

# 复制代码
# if __name__ == '__main__':
#     # 实例化动物园
#     z = Zoo('时间动物园')
#     # 实例化一只猫，属性包括名字、类型、体型、性格
#     cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
#     # 增加一只猫到动物园
#     z.add_animal(cat1)
#     # 动物园是否有猫这种动物
#     have_cat = hasattr(z, 'Cat')
# 具体要求：

# 定义“动物”、“猫”、“狗”、“动物园”四个类，动物类不允许被实例化。
# 动物类要求定义“类型”、“体型”、“性格”、“是否属于凶猛动物”四个属性，是否属于凶猛动物的判断标准是：“体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。
# 猫类要求有“叫声”、“是否适合作为宠物”以及“名字”三个属性，其中“叫声”作为类属性，除凶猛动物外都适合作为宠物，猫类继承自动物类。狗类属性与猫类相同，继承自动物类。
# 动物园类要求有“名字”属性和“添加动物”的方法，“添加动物”方法要实现同一只动物（同一个动物实例）不能被重复添加的功能。

from abc import ABC,abstractmethod
#动物园
# 动物园类要求有“名字”属性和“添加动物”的方法，“添加动物”方法要实现同一只动物（同一个动物实例）不能被重复添加的功能。
class Zoo(object):
    def __init__(self,name,a_list=None):
        self.name = name
        if a_list is None:
            self.a_list = []
    def add_animal(self, Animal):      
        setattr(self,Animal.__class__.__name__,Animal)
        if Animal not in self.a_list:
            self.a_list.append(Animal)
        else:
            print(f"{Animal.__dict__['name']}已存在，不需要重复添加")


#动物
# 动物类要求定义“类型”、“体型”、“性格”、“是否属于凶猛动物”四个属性，是否属于凶猛动物的判断标准是：“体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。
class Animal(ABC):
    def __init__(self, name, a_type, shape, character):
        self.name = name
        self.a_type = a_type
        self.shape = shape
        self.character = character
    
    @abstractmethod
    def is_terrible(self, a_type, shape, character):
        pass

#猫
# 猫类要求有“叫声”、“是否适合作为宠物”以及“名字”三个属性，其中“叫声”作为类属性，除凶猛动物外都适合作为宠物，猫类继承自动物类。
class Cat(Animal):
    sound = 'miao'
    def __init__(self, name, a_type, shape, character):
        super().__init__(name, a_type, shape, character)
    @property
    def is_terrible(self):
        shape_dict = {"小":1, "中等":2, "大":3}
        if shape_dict[self.shape] >= 2 and self.a_type == '食肉' and self.character == '凶猛':
            return True
        else:
            return False
    @property
    def is_suit_pet(self):
        if self.is_terrible:
            return "不适合做宠物"
        else:
            return "适合做宠物"

#狗
#狗类属性与猫类相同，继承自动物类。
class dog(Animal):
    sound = 'wang'
    def __init__(self, name, a_type, shape, character):
        super().__init__(name, a_type, shape, character)

    @property
    def is_terrible(self):
        shape_dict = {"小":1, "中等":2, "大":3}
        if shape_dict[self.shape] >= 2 and self.a_type == '食肉' and self.character == '凶猛':
            return True
        else:
            return False

    @property
    def is_suit_pet(self):
        if self.is_terrible:
            return "不适合做宠物"
        else:
            return "适合做宠物"



if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')
