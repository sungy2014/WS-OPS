/*
 * passwordStrength
 * Version: 1.2.1
 *
 * A simple plugin that can test the strength of password
 *
 * https://github.com/HenriettaSu/passwordStrength
 *
 * License: MIT
 *
 * Released on: November 22, 2016
 */

$.fn.passwordStrength = function (option) {
    var ele = $(this);
    settings = $.extend($.tester.defaultSettings, option);
    tester = new $.tester(ele, settings);
    return tester;
}

$.tester = function (ele, settings) {
    this.selector = ele;
    this.init(ele, settings);
}

$.extend($.tester, {
    defaultRules: {
        number: {
            rule: /\d+/,
            method: true
        },
        lowercase: {
            rule: /[a-z]+/,
            method: true
        },
        uppercase: {
            rule: /[A-Z]+/,
            method: true
        },
        speChar: {
            rule: /[#@!~_\-%^&*()\\\/]/,
            method: true
        },
        len: {
            rule: /\S{12,}/,
            method: true
        },
        same: {
            rule: /^(.)\1{2,}$/,
            method: false
        }
    },
    defaultSettings: {
        gradeClass: {
            bad: 'bg-red',
            pass: 'bg-orange',
            good: 'bg-green'
        }
    },
    prototype: {
        init: function (ele, settings) {
            var eleName = ele.attr('name'),
                rules = $.tester.defaultRules,
                progress = '<div class="password-progress"><div data-name="' + eleName + '" class="progress-bar" style="width: 0%;"></div></div>',
                $progress;
            ele.after(progress);
            $progress = $('.progress-bar[data-name="' + eleName + '"]');
            ele.on('keyup.passwordStrength', function () {
                var $this = $(this),
                    val = $this.val(),
                    strength = 0,
                    scroe,
                    per,
                    colorClass,
                    i,
                    rule,
                    method,
                    ruleLength = 0;
                for (i in rules) {
                    rule = rules[i].rule;
                    method = rules[i].method;
                    if (val.match(rule)) {
                        strength += (method === true) ? 1 : (method === false) ? -1 : 0;
                    }
                    ruleLength += (method === true) ? 1 : 0;
                }
                scroe = 100 / ruleLength;
                per = strength * scroe;
                colorClass = (per < 30) ? settings.gradeClass.bad : (per > 30 && per < 90) ? settings.gradeClass.pass : settings.gradeClass.good;
                $progress.css('width', per + '%');
                $progress.attr('class', 'progress-bar ' + colorClass);
            });
        },
        reset: function () {
            var selector = this.selector,
                eleName = $(selector[0]).attr('name'),
                $progress = $('.progress-bar[data-name="' + eleName + '"]');
            selector.val('');
            $progress.css('width', '0');
            $progress.attr('class', 'progress-bar');
        },
        destroy: function () {
            var selector = this.selector,
                eleName = $(selector[0]).attr('name'),
                $progress = $('.progress-bar[data-name="' + eleName + '"]').parent();
            $progress.remove();
            selector.off('keyup.passwordStrength');
            delete this.selector;
        }
    },
    addRules: function (rules) {
        $.extend($.tester.defaultRules, rules);
    }
});
