import struct


SPACER = '-'*50


# noinspection SpellCheckingInspection,PyPep8Naming
class ssSEQ:
    __SEQDATA_INFO_LAYOUTS = {
        101: {
            'name': "Legacy",
            'padd_size': 0
        },

        102: {
            'name': "Latest",
            'padd_size': 4
        }
    }

    __SEQDATA_INFO_TYPES = {
        104: {
            'name': "Easy",
            'lanes': range(0, 13, 4)
        },
        107: {
            'name': "Normal",
            'lanes': range(0, 13, 2)
        },
        113: {
            'name': "Hard",
            'lanes': range(13)
        }
    }

    __SEQDATA_EVENT_PROPERTIES = {
        0: "Tap",
        11: "Group 1 Slider Start",
        12: "Group 1 Slider Continue",
        3: "Group 1 Slider Continue",
        21: "Group 2 Slider Start",
        22: "Group 2 Slider Continue",
        232: "Group 3 Slider Start",
        233: "Group 3 Slider Continue",
    }

    # noinspection PyDictCreation
    def __init__(self, seq_file):
        # Helper functions
        def read_int(buffer):
            return struct.unpack('i', buffer.read(4))[0]

        def read_float(buffer):
            return struct.unpack('f', buffer.read(4))[0]

        def read_double(buffer):
            return struct.unpack('d', buffer.read(8))[0]

        def skip_padding(buffer, layout):
            buffer.seek(self.__SEQDATA_INFO_LAYOUTS[layout]['padd_size'], 1)

        with open(seq_file, 'rb') as seq:
            # Info such as layout, length, count of various things, and difficulty
            self.__SEQData_Info = {}
            self.__SEQData_Info['layout'] = read_int(seq)
            self.__SEQData_Info['tickLength'] = read_int(seq)
            self.__SEQData_Info['secLength'] = read_double(seq)
            self.__SEQData_Info['tickPerBeat'] = read_int(seq)
            skip_padding(seq, self.__SEQData_Info['layout'])  # padd_0
            self.__SEQData_Info['beatPerTick'] = read_double(seq)
            self.__SEQData_Info['tempoCount'] = read_int(seq)
            self.__SEQData_Info['objectCount'] = read_int(seq)
            self.__SEQData_Info['channelCount'] = read_int(seq)
            self.__SEQData_Info['eventCount'] = read_int(seq)
            self.__SEQData_Info['measureCount'] = read_int(seq)
            self.__SEQData_Info['beatCount'] = read_int(seq)
            self.__SEQData_Info['type'] = read_int(seq)
            skip_padding(seq, self.__SEQData_Info['layout'])  # padd_1

            # Tempo sections of the beatmap
            self.__SEQData_Tempo = []
            for i in range(self.__SEQData_Info['tempoCount']):
                __tempo = {}
                __tempo['tick'] = read_int(seq)
                __tempo['tickEnd'] = read_int(seq)
                __tempo['sec'] = read_float(seq)
                __tempo['secEnd'] = read_float(seq)
                __tempo['beatPerMinute'] = read_double(seq)
                __tempo['beatPerMeasure'] = read_int(seq)
                skip_padding(seq, self.__SEQData_Info['layout'])  # padd_0
                __tempo['measurePerBeat'] = read_double(seq)
                __tempo['measurePerTick'] = read_double(seq)
                __tempo['tickPerMeasure'] = read_int(seq)
                skip_padding(seq, self.__SEQData_Info['layout'])  # padd_1
                __tempo['beatPerSec'] = read_double(seq)
                __tempo['secPerBeat'] = read_double(seq)
                __tempo['tickPerSec'] = read_double(seq)
                __tempo['secPerTick'] = read_double(seq)
                __tempo['measurePerSec'] = read_double(seq)
                __tempo['secPerMeasure'] = read_double(seq)
                __tempo['measureStart'] = read_int(seq)
                __tempo['measureCount'] = read_int(seq)
                self.__SEQData_Tempo.append(__tempo)

            # This part is a bit wonky
            # File names and comments
            self.__SEQData_Object = []
            __last_object: dict = {}
            __last_object['dataLen'] = read_int(seq)
            if __last_object['dataLen']:
                __last_object['data'] = seq.read(__last_object['dataLen']).decode('UTF-8')
            for i in range(self.__SEQData_Info['objectCount'] - 1):
                # Not sure what property does
                __object: dict = {}
                __object['property'] = read_int(seq)
                __object['dataLen'] = read_int(seq)
                if __object['dataLen']:
                    __object['data'] = seq.read(__object['dataLen']).decode('UTF-8')
                    self.__SEQData_Object.append(__object)
            __last_object['property'] = read_int(seq)
            if __last_object['dataLen']:
                __last_object = {'property': __last_object.pop('property'), **__last_object}
                self.__SEQData_Object.append(__last_object)

            # Event count in each channel
            self.__SEQData_Channel = []
            for i in range(self.__SEQData_Info['channelCount']):
                # Not sure what property does
                __channel = {}
                __channel['eventCount'] = read_int(seq)
                __channel['property'] = read_int(seq)
                self.__SEQData_Channel.append(__channel)

            # Marking events
            self.__SEQData_Event = []
            self.__start_event = False
            self.__end_event = False
            self.__noteCount = 0
            self.__noteCountUncheck = 0
            self.__invalid = 0
            for i in range(self.__SEQData_Info['eventCount']):
                # Not sure what duration, objectId, and property do
                __event = {}
                __event['tick'] = read_int(seq)
                __event['duration'] = read_int(seq)
                __event['channelId'] = read_int(seq)
                __event['objectId'] = read_int(seq)
                __event['property'] = read_int(seq)

                if i == 0:
                    if __event['duration'] == 0 and __event['channelId'] == 31 and __event['objectId'] == 1:
                        # and __event['property'] == 0
                        __event['note'] = "start"
                        self.__start_event = True
                    else:
                        __event['note'] = "invalid"
                        self.__invalid += 1
                elif i == self.__SEQData_Info['eventCount'] - 1:
                    if __event['duration'] == 0 and __event['channelId'] == 13 and __event['objectId'] == 0 \
                            and __event['property'] == 0:
                        __event['note'] = "end"
                        self.__end_event = True
                    else:
                        __event['note'] = "invalid"
                        self.__invalid += 1
                else:
                    if __event['tick'] in range(self.__SEQData_Info['tickLength']) and __event['duration'] == 0 \
                            and __event['channelId'] in self.__SEQDATA_INFO_TYPES[self.__SEQData_Info['type']]['lanes']:
                        # and event['objectId'] in (0, 2, 5, 8, 15, 16, 30, 34)
                        if __event['property'] in self.__SEQDATA_EVENT_PROPERTIES:
                            __event['note'] = self.__SEQDATA_EVENT_PROPERTIES[__event['property']]
                            self.__noteCount += 1
                            self.__noteCountUncheck += 1
                        else:
                            __event['note'] = "unknown"
                            self.__noteCountUncheck += 1
                    else:
                        __event['note'] = "invalid"
                        self.__invalid += 1
                skip_padding(seq, self.__SEQData_Info['layout'])
                self.__SEQData_Event.append(__event)

    def __repr__(self):
        # Info
        __strs = ["SEQData_Info", SPACER]
        for __info in self.__SEQData_Info:
            __temp = f"{__info}: {self.__SEQData_Info[__info]}"
            if __info == 'layout':
                __temp += f" ({self.__SEQDATA_INFO_LAYOUTS[self.__SEQData_Info[__info]]['name']})"
            elif __info == 'beatCount' and self.__SEQData_Info[__info] == 0 and self.__SEQData_Info['tempoCount'] > 1:
                __temp += " (multi-tempo)"
            elif __info == 'type':
                __temp += f" ({self.__SEQDATA_INFO_TYPES[self.__SEQData_Info[__info]]['name']})"
            __strs.append(__temp)
        __strs.append('')

        # Tempo
        __strs.extend(("SEQData_Tempo", SPACER))
        for __tempo in range(self.__SEQData_Info['tempoCount']):
            __strs.extend((f"tempoId {__tempo}", SPACER))
            for __info in self.__SEQData_Tempo[__tempo]:
                __strs.append(f"{__info}: {self.__SEQData_Tempo[__tempo][__info]}")
            __strs.append('')

        # Channel
        __strs.extend(("SEQData_Object", SPACER))
        for __object in range(len(self.__SEQData_Object)):
            __strs.extend((f"objectId {__object}", SPACER))
            for __info in self.__SEQData_Object[__object]:
                __strs.append(f"{__info}: {self.__SEQData_Object[__object][__info]}")
            __strs.append('')

        # Channel
        __strs.extend(("SEQData_Channel", SPACER))
        __eventCount_channel = 0
        for __channel in range(self.__SEQData_Info['channelCount']):
            __strs.append(f"channelId {__channel}: {self.__SEQData_Channel[__channel]}")
            __eventCount_channel += self.__SEQData_Channel[__channel]['eventCount']

        if __eventCount_channel != self.__SEQData_Info['eventCount']:
            __strs.append(f"\nWarning: SEQData_Channel's eventCount ({__eventCount_channel}) is not equal to "
                          f"SEQData_Info's eventCount ({self.__SEQData_Info['eventCount']}).")
        __strs.append('')

        # Event
        __strs.extend(("SEQData_Event", SPACER))
        __eventCount_event = {}
        for __event in self.__SEQData_Event:
            if __event['channelId'] not in __eventCount_event:
                __eventCount_event[__event['channelId']] = 1
            else:
                __eventCount_event[__event['channelId']] += 1
            __strs.append(str(__event))

        if not self.__start_event:
            __strs.append("\nWarning: Start event does not exist.")
        if not self.__end_event:
            __strs.append("\nWarning: End event does not exist.")

        for __channel in range(self.__SEQData_Info['channelCount']):
            if __channel not in __eventCount_event:
                __eventCount_event[__channel] = 0
            if __eventCount_event[__channel] != self.__SEQData_Channel[__channel]['eventCount']:
                __strs.append(f"\nWarning: channelId {__channel}: SEQData_Event's eventCount "
                              f"({__eventCount_event[__channel]}) is not equal to SEQData_Channel's eventCount "
                              f"({self.__SEQData_Channel[__channel]['eventCount']}).")

        __strs.append(f"\nnoteCount: {self.__noteCount}")
        __strs.append(f"noteCountUncheck: {self.__noteCountUncheck}")
        __strs.append(f"invalid: {self.__invalid}")

        return '\n'.join(__strs)

    def __str__(self):
        return f"{self.__SEQData_Object[0]['data']}: {self.__noteCount} / {self.__noteCountUncheck} " \
               f"(invalid: {self.__invalid})"
